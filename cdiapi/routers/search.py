from typing import List, Optional, Union
from fastapi import APIRouter, Path, Query, Response, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
import meilisearch

from cdiapi import settings
from cdiapi.logs import get_logger
from cdiapi.data.common import ErrorResponse
from cdiapi.data.common import SearchIndexEntryResponse, SearchIndexSearchResponse
import motor.motor_asyncio
log = get_logger(__name__)
router = APIRouter()


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.cdisearch

DEFAULT_URL = 'https://localhost:7090'

class MeiliWrapper:
    def __init__(self, url:str=DEFAULT_URL, key:str=None, index_name:str=None):        
        self.client = meilisearch.Client(url, key)
        self.m_index = self.client.index(index_name) if index_name is not None else None


@router.get(
    "/search/0.1/entry/{entry_id}",
    tags=["search", 'search index'],
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
    "/index/0.1/query",
    tags=["search", 'search index'],
    response_model=SearchIndexSearchResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Object not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)


async def search_entries(
    response: Response,
    q: str = Query("", title="Query text, for example: 'Atlantic salmon'"),
    filters: List[str] = Query([], title="Filters by vacets value. Should be like \"source.catalog_type\"=\"Geoportal\" "),
    limit: int = Query(1000, title="Number of results to return", le=settings.MAX_PAGE),
    offset: int = Query(
        0, title="Start at result with given offset", le=settings.MAX_OFFSET
    ),
    page: int = Query(
        1, title="Page number"
    ),
    facets:bool = Query(True, title="Enable/Disable facets output"),
    sort_by:str=Query(settings.DEFAULT_SORT, title="Sort by fields, default 'scores.feature_score:desc'. Use single field or list of fields divided by comma. Supported fields: 'scores.feature_score', 'dataset.title', 'source.uid'")    
) -> Union[RedirectResponse, JSONResponse]:
    """Dataset search).
    """    
    wrapper = MeiliWrapper(settings.MEILI_URL, settings.MEILI_KEY, index_name=settings.MEILI_INDEX)
    params = {'offset' : offset, 'limit' : limit, 'filter' : filters, 
                'hitsPerPage' : 20, 'sort' : sort_by.split(','), 'page' : page}
    if facets:
        params['facets'] = settings.DEFAULT_FACETS
    results = wrapper.m_index.search(q, params)
    return JSONResponse(results)

