import datetime

from pydantic import BaseModel
from pydantic import Field

from .users import UsersListElementModel
from .users import PaginatedMetaDataModel


class CitiesHintModel(BaseModel):
    id: int = Field(..., description="Id")
    name: str = Field(..., description="Name")


class PrivateUsersListHintMetaModel(BaseModel):
    city: list[CitiesHintModel] = Field(..., description="City")


class PrivateUsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel = Field(..., description="Pagination")
    hint: PrivateUsersListHintMetaModel = Field(..., description="Hint")


class PrivateUsersListResponseModel(BaseModel):
    data: list[UsersListElementModel] = Field(..., description="Data")
    meta: PrivateUsersListMetaDataModel = Field(..., description="Meta")


class PrivateCreateUserModel(BaseModel):
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")
    other_name: str = Field(None, description="Other Name")
    email: str = Field(..., description="Email")
    phone: str = Field(None, description="Phone")
    birthday: datetime.date = Field(None, description="Birthday")
    is_admin: bool = Field(..., description="Is Admin")
    city: int = Field(None, description="City")
    additional_info: str = Field(None, description="Additional Info")
    password: str = Field(..., description="Password")

    class Config:
        orm_mode = True


class PrivateDetailUserResponseModel(BaseModel):
    id: int = Field(..., description="Id")
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")
    other_name: str = Field(None, description="Other Name")
    email: str = Field(..., description="Email")
    phone: str = Field(None, description="Phone")
    birthday: datetime.date = Field(None, description="Birthday")
    is_admin: bool = Field(..., description="Is Admin")
    city: int = Field(None, description="City")
    additional_info: str = Field(None, description="Additional Info")

    class Config:
        orm_mode = True


class PrivateUpdateUserModel(BaseModel):
    first_name: str = Field(None, description="First Name")
    last_name: str = Field(None, description="Last Name")
    other_name: str = Field(None, description="Other Name")
    email: str = Field(None, description="Email")
    phone: str = Field(None, description="Phone")
    birthday: datetime.date = Field(None, description="Birthday")
    is_admin: bool = Field(None, description="Is Admin")
    city: int = Field(None, description="City")
    additional_info: str = Field(None, description="Additional Info")

    class Config:
        orm_mode = True
