from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from . import responses

from .dependencies import check_password
from .dependencies import create_temp_token

from ..models import LoginModel
from ..models import CurrentUserResponseModel

from ...db import queries_users

router = APIRouter(tags=["auth"])


@router.post(
    "/login",
    summary="Вход в систему",
    responses=responses.LOGIN,
    response_model=CurrentUserResponseModel,
)
async def login(login_data: Annotated[LoginModel, Body()]):
    """
    Создана для входа пользователя в систему.
    """
    if not await queries_users.check_in_table(login_data.login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not await check_password(login_data.login, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password"
        )

    user = await queries_users.get_user_by_email(login_data.login)
    user_model = CurrentUserResponseModel(
        first_name=user.first_name,
        last_name=user.last_name,
        other_name=user.other_name,
        email=user.email,
        phone=user.phone,
        birthday=user.birthday,
        is_admin=user.is_admin,
    )
    token = await create_temp_token(login_data.login)
    user_model = jsonable_encoder(user_model)

    response = JSONResponse(content=user_model)
    response.set_cookie(key="access_token", value=token)

    return response


@router.get("/logout", summary="Выход из системы", responses=responses.LOGOUT)
async def logout() -> JSONResponse:
    """
    Создана для выхода пользователя из ситемы.
    """

    response = JSONResponse(content="OK")
    response.set_cookie(key="access_token", value=None)
    return response
