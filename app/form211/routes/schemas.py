from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateForm211Request(BaseModel):
    name: str
    created_by: int
    operational_period: int


class CreateForm211Response(BaseModel):
    id: int
    created_by: int
    name: str
    operational_period: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime


class RetrieveForm211Response(BaseModel):
    id: int
    created_by: int
    name: str
    operational_period: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime


class ListForm211ResponseItem(BaseModel):
    id: int
    created_by: int
    name: str
    operational_period: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime


class ListForm211Response(BaseModel):
    count: int
    items: list[ListForm211ResponseItem]


class UpdateForm211Request(BaseModel):
    name: str


class UpdateForm211Response(BaseModel):
    created_by: int
    name: str
    operational_period: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime


class SignInForm211Request(BaseModel):
    sar_id: int
    name: str
    created_by: int


class SignInForm211Response(BaseModel):
    id: int
    form211_id: int
    created_by: int
    sar_id: int
    name: str
    resource_type: str
    arrival_at: datetime
    departure_at: Optional[datetime] = None


class SignOutForm211Request(BaseModel):
    sar_id: int


class SignOutForm211Response(BaseModel):
    id: int
    form211_id: int
    created_by: int
    sar_id: int
    name: str
    resource_type: str
    arrival_at: datetime
    departure_at: Optional[datetime] = None


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
