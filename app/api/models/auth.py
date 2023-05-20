import datetime

from pydantic import BaseModel
from pydantic import Field


class LoginModel(BaseModel):
    login: str = Field(..., description="Login")
    password: str = Field(..., description="Password")


class CurrentUserResponseModel(BaseModel):
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")
    other_name: str = Field(None, description="Other Name")
    email: str = Field(..., description="Email")
    phone: str = Field(None, description="Phone")
    birthday: datetime.date = Field(None, description="Birthday")
    is_admin: bool = Field(..., description="Is Admin")

    class Config:
        orm_mode = True
