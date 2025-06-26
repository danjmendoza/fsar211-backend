from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateTimelogRequest(BaseModel):
    form211_id: int
    sar_id: int
    created_by: Optional[int]
    name: str
    resource_type: str
    arrival_at: Optional[datetime]
    departure_at: Optional[datetime]


class CreateTimelogResponse(BaseModel):
    id: int
    form211_id: int
    sar_id: int
    created_by: Optional[int]
    name: str
    resource_type: str
    arrival_at: datetime
    departure_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class RetrieveTimelogResponse(BaseModel):
    id: int
    form211_id: int
    sar_id: int
    created_by: Optional[int]
    name: str
    resource_type: str
    arrival_at: Optional[datetime]
    departure_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class ListTimelogResponseItem(BaseModel):
    id: int
    form211_id: int
    sar_id: int
    created_by: Optional[int]
    name: str
    resource_type: str
    arrival_at: Optional[datetime]
    departure_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class ListTimelogResponse(BaseModel):
    count: int
    items: list[ListTimelogResponseItem]


class UpdateTimelogRequest(BaseModel):
    form211_id: int
    sar_id: int
    created_by: Optional[int]
    name: str
    resource_type: str
    arrival_at: Optional[datetime]
    departure_at: Optional[datetime]


class UpdateTimelogResponse(BaseModel):
    id: int
    form211_id: int
    sar_id: int
    created_by: Optional[int]
    name: str
    resource_type: str
    arrival_at: Optional[datetime]
    departure_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
