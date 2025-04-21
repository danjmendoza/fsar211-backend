from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str
    resource_type: str

    class Config:
        orm_mode = True


class CreatePost(UserBase):
    class Config:
        orm_mode = True