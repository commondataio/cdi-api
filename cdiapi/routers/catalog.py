from typing import List, Optional, Union
from fastapi import APIRouter, Path, Query, Response, HTTPException
from fastapi.responses import RedirectResponse

from cdiapi import settings
from cdiapi.logs import get_logger
from cdiapi.data.common import ErrorResponse
from cdiapi.data.common import DataCatalogResponse, DataCatalogSearchResponse
import motor.motor_asyncio
log = get_logger(__name__)
router = APIRouter()


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.cdi


@router.get(
    "/catalog/{catalog_id}",
    tags=["Data catalogs registry"],
    response_model=DataCatalogResponse,
    responses={
        307: {"description": "The data catalog was merged into another ID"},
        404: {"model": ErrorResponse, "description": "Object not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def fetch_datacatalog(
    response: Response,
    catalog_id: str = Path(
        description="UID of the data catalog to retrieve", examples=["cdi00000006"], default=None
    ),
) -> Union[RedirectResponse, DataCatalogResponse]:
    """Retrieve a single data catalog registry item by its UID. The record will be returned in
    full. If the catalog has been merged into a another catalog canonical entity, an HTTP redirect will
    be triggered.

    Intro: [data catalog records](https://commondata.io/docs/datacatalog).
    """
    item = await db["catalogs"].find_one({'uid' : catalog_id})
    if item is None:
        raise HTTPException(404, detail="No such data catalog!")
    log.info(item['name'], action="catalog", catalog_id=catalog_id)
    response.headers.update(settings.CACHE_HEADERS)
    return item


@router.get(
    "/search/catalogs/",
    tags=["Data catalogs registry"],
    response_model=DataCatalogSearchResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Object not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def fetch_datacatalog(
    response: Response,
    q: str = Query("", title="Query text"),
    limit: int = Query(10, title="Number of results to return", le=settings.MAX_PAGE),
    offset: int = Query(
        0, title="Start at result with given offset", le=settings.MAX_OFFSET
    ),
    software: str = Query(None, title="Software identifier"),
    owner_type: str = Query(None, title="Owner type"),
    catalog_type: str = Query(None, title="Owner type"),
    owner_country: List[str] = Query([], title="Country of the owner"),
    coverage_country: List[str] = Query([], title="Country of the coverage"),

) -> Union[RedirectResponse, DataCatalogSearchResponse]:
    """Retrieve a list of data catalog registry item.

    Intro: [data catalog records](https://commondata.io/docs/datacatalog).
    """
    query = {}
    if q: query['$text'] = {'$search' : q}
    if software: query['software.id'] = software
    if owner_type: query['owner_type'] = owner_type
    if catalog_type: query['catalog_type'] = catalog_type
    if owner_country: query['owner.location.country'] = {'$in': owner_country}
    if coverage_country: query['coverage.location.country'] = {'$in': coverage_country}
    total = await db['catalogs'].count_documents({})
    items = await db["catalogs"].find(query, {'uid' : 1, 'name' : 1, 'link' : 1}).skip(offset).limit(limit).to_list(limit)
    if items is None or len(items) == 0:
        raise HTTPException(404, detail="No such data catalog!")
    log.info(str(query), action="catalogsearch", search_query=query)
    response.headers.update(settings.CACHE_HEADERS)
    meta = {'offset' : offset, 'limit' : limit, 'num' : len(items), 'total': total}
    response = {'meta' : meta, 'data' : items} 
    return response

