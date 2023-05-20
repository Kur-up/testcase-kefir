import datetime

from pydantic import BaseModel
from pydantic import Field


class UpdateUserModel(BaseModel):
    first_name: str = Field(None, description="First Name")
    last_name: str = Field(None, description="Last Name")
    other_name: str = Field(None, description="Other Name")
    email: str = Field(None, description="Email")
    phone: str = Field(None, description="Phone")
    birthday: datetime.date = Field(None, description="Birthday")

    class Config:
        orm_mode = True


class UpdateUserResponseModel(UpdateUserModel):
    id: int = Field(..., description="Id")


class UsersListElementModel(BaseModel):
    id: int = Field(..., description="Id")
    first_name: str = Field(None, description="First Name")
    last_name: str = Field(None, description="Last Name")
    email: str = Field(None, description="Email")


class PaginatedMetaDataModel(BaseModel):
    total: int = Field(..., description="Total")
    page: int = Field(..., description="Page")
    size: int = Field(..., description="Size")


class UsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel = Field(..., description="Pagination")


class UsersListResponseModel(BaseModel):
    data: list[UsersListElementModel] = Field(..., description="Data")
    meta: UsersListMetaDataModel = Field(..., description="Meta")
