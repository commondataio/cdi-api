from datetime import datetime
from typing import Dict, List, Union, Optional
from pydantic import BaseModel, Field

from .shared import SpokenLanguage, Location, Topic, Endpoint, Identifier, Organization, Software, Country, SubRegion, MacroRegion

class SearchIndexSourceRecord(BaseModel):
    uid: str = Field(..., examples=["cdi00001616"])
    name: str = Field(..., examples=["Data.gov portal"])
    url: str = Field(..., examples=["https://catalog.data.gov"])
    catalog_type: str = Field(..., examples=["Open data portal"])
    langs: List[SpokenLanguage] = Field([], examples=[])
    owner_name: str = Field(..., examples=["USA Government"])
    owner_type: str = Field(..., examples=["Central government"])
    software: Software = Field(..., examples=["CKAN"])
    countries: List[Country] = Field([], examples=[])
    macroregions: List[MacroRegion] = Field([], examples=[])
    subregions: List[SubRegion] = Field([], examples=[])


class SearchIndexParty(BaseModel):
    id: Optional[str] = Field(None, examples=["abu-dhabi-agriculture-and-food-safety-authority"])
    title: str = Field(..., examples=["Abu Dhabi Agriculture And Food Safety Authority"])
    role: str = Field(..., examples=["Publisher"])

class SearchIndexDatasetRecord(BaseModel):
    id: str = Field(..., examples=[""])
    title: str = Field(None, examples=["Name of the dataset"])
    num_resources: int = Field(..., examples=["1"])
    url: str = Field(..., examples=["https://data.bayanat.ae/dataset/open-field-exposed-vegetable-crops"])
    short_text: Optional[str] = Field(None, examples=["Short plain text, extracted from description"])
    description: Optional[str] = Field(None, examples=["Some dataset text description. Originally could be HTML or any other text"])
    has_archive: bool = Field(False, examples=['False'])
    tags: Optional[List[str]] = Field(None, examples=['Farm', "Crops"])
    formats: Optional[List[str]] = Field([], examples=['XLSX', "CSV"])
    datatypes: Optional[List[str]] = Field([], examples=['data', "geodata"])
    topics_origial: Optional[List[str]] = Field(None, examples=['Farm', "Crops"])
    responsible: List[SearchIndexParty] = Field(None, examples=[])
    license_id: Optional[str] = Field(None, examples=["cc-by"])
    license_name: Optional[str] = Field(None, examples=["Creative Commons Attribution"])
    license_url: Optional[str] = Field(None, examples=[])

class SearchIndexResourceRecord(BaseModel):
    id: Optional[str] = Field(None, examples=["f7ddcec7-5f5a-4458-8b10-ec8fd2d4a93b"])
    name: Optional[str] = Field(None, examples=["Data.gov portal"])
    datasize: Optional[str] = Field(None, examples=["100000"])
    format: Optional[str] = Field(None, examples=["XLSX"])
    mimetype: Optional[str] = Field(None, examples=["application/vnd.excel"])
    url: Optional[str] = Field(None, examples=["http://data.bayanat.ae/en_GB/dataset/c4a88574-7a2a-4048-bc9f-07de0559e7b7/resource/f7ddcec7-5f5a-4458-8b10-ec8fd2d4a93b/download/open-field-_exposed_-vegetable-crops.xlsx"])



class SearchIndexEntry(BaseModel):
    id: str = Field(..., examples=["cdi00000002-c4a88574-7a2a-4048-bc9f-07de0559e7b7"])
    int_id: Optional[str] = Field(..., examples=["c4a88574-7a2a-4048-bc9f-07de0559e7b7"])
    source: SearchIndexSourceRecord = Field(..., examples=[])
    dataset: SearchIndexDatasetRecord = Field(..., examples=[])
    resources: List[SearchIndexResourceRecord] = Field(..., examples=[])

EXAMPLE_SEARCH_ENTRY = """{
  "_id": {
    "$oid": "6495ab04180d222d037c0649"
  },
  "source": {
    "uid": "cdi00000002",
    "name": "UAE Open Data Portal",
    "catalog_type": "Open data portal",
    "owner_name": "Government of UAE",
    "owner_type": "Central government",
    "url": "https://data.bayanat.ae",
    "software": "CKAN",
    "langs": [
      "EN"
    ],
    "countries": [
      "United Arab Emirates"
    ]
  },
  "dataset": {
    "id": "c4a88574-7a2a-4048-bc9f-07de0559e7b7",
    "num_resources": 1,
    "url": "https://data.bayanat.ae/dataset/open-field-exposed-vegetable-crops",
    "title": "Open Field \"Exposed\" Vegetable Crops",
    "description": "The dataset show the area (donum) and distribution of Open Field \"Exposed\" Vegetable Crops land in the Emirate of Abu Dhabi\r\n",
    "has_archive": false,
    "responsible": [
      {
        "title": "Abu Dhabi Agriculture And Food Safety Authority ",
        "id": "abu-dhabi-agriculture-and-food-safety-authority",
        "role": "Publisher"
      }
    ],
    "topics_original": [
      "الزراعة"
    ],
    "formats": [
      "XLSX"
    ],
    "tags": [
      "Farms",
      "Forest Trees",
      "Fruit Trees Crops",
      "Vegetable Crops",
      "agriculture",
      "area",
      "field",
      "land uses"
    ],
    "license_id": "cc-by",
    "license_name": "Creative Commons Attribution",
    "license_url": null
  },
  "resources": [
    {
      "id": "f7ddcec7-5f5a-4458-8b10-ec8fd2d4a93b",
      "name": "Open Field _Exposed_ Vegetable Crops.",
      "datasize": null,
      "format": "XLSX",
      "mimetype": null,
      "url": "http://data.bayanat.ae/en_GB/dataset/c4a88574-7a2a-4048-bc9f-07de0559e7b7/resource/f7ddcec7-5f5a-4458-8b10-ec8fd2d4a93b/download/open-field-_exposed_-vegetable-crops.xlsx"
    }
  ],
  "int_id": "c4a88574-7a2a-4048-bc9f-07de0559e7b7"
  "id": "cdi00000002-c4a88574-7a2a-4048-bc9f-07de0559e7b7"
}
"""