from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str
    resource_type: str
    sar_id: int


class CreateUserResponse(BaseModel):
    id: int
    name: str
    sar_id: Optional[int]
    email: str
    resource_type: str
    created_at: datetime
    updated_at: datetime


class RetrieveUserResponse(BaseModel):
    id: int
    sar_id: Optional[int]
    name: str
    email: str
    resource_type: str
    created_at: datetime
    updated_at: datetime


class ListUsersResponseItem(BaseModel):
    id: int
    name: str
    sar_id: Optional[int]
    email: str
    resource_type: str
    created_at: datetime
    updated_at: datetime


class ListUsersResponse(BaseModel):
    count: int
    items: list[ListUsersResponseItem]


class UpdateUserRequest(BaseModel):
    name: str
    sar_id: Optional[int]
    email: str
    resource_type: str


class UpdateUserResponse(BaseModel):
    id: int
    name: str
    sar_id: Optional[int]
    email: str
    resource_type: str
    created_at: datetime
    updated_at: datetime
