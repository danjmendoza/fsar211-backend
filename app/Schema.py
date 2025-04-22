from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    resource_type: str

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    class Config:
        from_attributes = True