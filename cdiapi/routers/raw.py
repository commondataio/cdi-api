from typing import List, Optional, Union
from fastapi import APIRouter, Path, Query, Response, HTTPException
from fastapi.responses import RedirectResponse

from cdiapi import settings
from cdiapi.logs import get_logger
from cdiapi.data.common import ErrorResponse
from cdiapi.data.common import SearchIndexEntryResponse, SearchIndexSearchResponse
import motor.motor_asyncio
log = get_logger(__name__)
router = APIRouter()


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.cdisearch


@router.get(
    "/raw/0.1/entry/{entry_id}",
    tags=["Search index data access"],
    response_model=SearchIndexEntryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Object not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def fetch_entry(    
    response: Response,
    entry_id: str = Path(
        description="Search index single entry", examples=["c4a88574-7a2a-4048-bc9f-07de0559e7b7"]
    ),
) -> Union[RedirectResponse, SearchIndexEntryResponse]:
    """Retrieve a single dataset
    """
    item = await db["fulldb"].find_one({'id' : entry_id})
    if item is None:
        raise HTTPException(404, detail="No such entry!")
#    log.info(item['name'], action="searchentry", entry_id=entry_id)
    response.headers.update(settings.CACHE_HEADERS)
    return item



@router.get(
    "/raw/0.1/search",
    tags=["Search index data access"],
    response_model=SearchIndexSearchResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Object not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def search_entries(
    response: Response,
    q: str = Query("", title="Query text"),
    limit: int = Query(10, title="Number of results to return", le=settings.MAX_PAGE),
    offset: int = Query(
        0, title="Start at result with given offset", le=settings.MAX_OFFSET
    ),
    software: str = Query(None, title="Software identifier"),
    owner_type: str = Query(None, title="Owner type"),
    catalog_type: str = Query(None, title="Owner type"),
    topics: List[str] = Query([], title="EU Data themes"),
    geotopics: List[str] = Query([], title="Geo topics"),
    countries: List[str] = Query([], title="Country of the owner"),
    langs: List[str] = Query([], title="Spoken languages"),
    tags: List[str] = Query([], title="Tags"),
) -> Union[RedirectResponse, SearchIndexSearchResponse]:
    """Dataset search).
    """
    query = {}
    if q: query['$text'] = {'$search' : q}
    if software: query['source.software.id'] = software
    if owner_type: query['source.owner_type'] = owner_type
    if catalog_type: query['source.catalog_type'] = catalog_type
    if countries: query['source.countries'] = {'$in': countries}
    if langs: query['source.langs.id'] = {'$in': langs}
    if tags: query['dataset.tags'] = {'$in': tags}
    if topics: query['dataset.topics'] = {'$in': topics}
    if geotopics: query['dataset.geotopics'] = {'$in': geotopics}
    total = await db['fulldb'].count_documents(query)
    items = await db["fulldb"].find(query, {}).skip(offset).limit(limit).to_list(limit)
    if items is None or len(items) == 0:
        raise HTTPException(404, detail="Nothing found")
    log.info(str(query), action="catalogsearch", search_query=query)
    response.headers.update(settings.CACHE_HEADERS)
    meta = {'offset' : offset, 'limit' : limit, 'num' : len(items), 'total': total}
    response = {'meta' : meta, 'data' : items} 
    return response

