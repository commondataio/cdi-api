import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from banal import as_bool
from os import environ as env
from normality import stringify
from datetime import datetime
from aiocron import Cron  # type: ignore


def env_str(name: str, default: Optional[str] = None) -> Optional[str]:
    """Ensure the env returns a string even on Windows (#100)."""
    value = stringify(env.get(name))
    return default if value is None else value


VERSION = "1.0.0"
AUTHOR = "Common Data Index"
HOME_PAGE = "https://commondata.io"
EMAIL = "info@commondata.io"
CONTACT = {"name": AUTHOR, "url": HOME_PAGE, "email": EMAIL}

TITLE = env_str("CDI_TITLE") or "Common Data Index"
DESCRIPTION = """
The Common Data Index API provides endpoints that help you to access registry of the data catalogs, raw indexes of metadata and search index.
"""

TAGS: List[Dict[str, Any]] = [
    {
        "name": "Data catalogs registry",
        "description": "Endpoints for for fetching data from Common Data Index registry of data catalogs",
        "externalDocs": {
            "description": "Data dictionary",
            "url": "https://commondata.io/docs",
        },
    },
    {
        "name": "System information",
        "description": "Service metadata endpoints for health checking and getting "
        "the application metadata to be used in client applications.",
    },
    {
        "name": "Raw data access",
        "description": "Endpoints for fetching raw metadata and data from the API, either related to "
        "individual data catalogs",
        "externalDocs": {
            "description": "Data dictionary",
            "url": "https://commondata.io/docs",
        },
    },
    {
        "name": "Search index data access",
        "description": "Endpoints for fetching raw metadata and data from the API, either related to "
        "search index",
        "externalDocs": {
            "description": "Data dictionary",
            "url": "https://commondata.io/docs",
        },
    },
    {
        "name": "Service API",
        "description": "Endpoints that help to identify datasets topis, licenses and other data matching tasks",
        "externalDocs": {
            "description": "Data dictionary",
            "url": "https://commondata.io/docs",
        },
    },
]

# Check if we're running in the context of unit tests:
TESTING = False
DEBUG = as_bool(env_str("CDIAPI_DEBUG", "true"))

MANIFEST_DEFAULT_PATH = Path(__file__).parent.parent / "manifests/default.yml"
MANIFEST = env_str("CDIAPI_MANIFEST") or str(MANIFEST_DEFAULT_PATH)

DATA_PATH = Path(env_str("CDIAPI_DATA_PATH") or "/tmp")
RESOURCES_PATH = Path(__file__).parent.joinpath("resources")

PORT = int(env_str("CDIAPI_PORT") or env_str("PORT") or "8000")
# How many results to return per page of search results max:
MAX_PAGE = 500

MAX_OFFSET = 100000

# ElasticSearch settings:
MEILI_URL = env_str("CDIAPI_MEILISEARCH_URL", "http://localhost:7700")
MEILI_KEY = env_str("CDIAPI_MEILISEARCH_KEY")

# Log output can be formatted as JSON:
LOG_JSON = as_bool(env_str("CDI_LOG_JSON", "false"))
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

# Used to pad out first_seen, last_seen on static collections
RUN_TIME = datetime.utcnow().isoformat()[:19]
# Cache headers
CACHE_HEADERS = {
    "Cache-Control": "public; max-age=3600",
    "X-Robots-Tag": "none",
}
