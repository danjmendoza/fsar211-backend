from datetime import datetime

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
