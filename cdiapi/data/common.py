from datetime import datetime
from typing import Dict, List, Union, Optional
from pydantic import BaseModel, Field

from cdiapi import settings
from .datacatalog import DataCatalog


class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["Detailed error message"])

DataCatalogResponse = DataCatalog



class SearchMeta(BaseModel):
    offset: int = Field(..., examples=['0'])
    limit: int = Field(..., examples=['100'])
    num: int = Field(..., examples=['15'])
    total: int = Field(..., examples=['1520'])

class DataCatalogSearchItem(BaseModel):
    uid: str = Field(..., examples=["cdi00001616"])
    name: str = Field(..., examples=["Data.gov portal"])
    link: str = Field(..., examples=["https://catalog.data.gov"])

class DataCatalogSearchResponse(BaseModel):
    meta: SearchMeta = Field(..., examples=[])
    data: List[DataCatalogSearchItem] = Field(..., examples=[])
