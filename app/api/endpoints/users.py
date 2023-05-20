from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body
from fastapi import Query
from fastapi import HTTPException
from fastapi import status

from . import responses

from .dependencies import check_authorization
from .dependencies import email_validation
from .dependencies import iso_date_validation

from ..models import UpdateUserModel
from ..models import UpdateUserResponseModel
from ..models import CurrentUserResponseModel
from ..models import UsersListResponseModel
from ..models import UsersListElementModel
from ..models import UsersListMetaDataModel
from ..models import PaginatedMetaDataModel

from ...db import queries_users
from ...db.core import UserAlchemy

router = APIRouter(tags=["user"])


@router.get(
    "/current",
    summary="Получение данных о текущем пользователе",
    responses=responses.USERS_CURRENT,
    response_model=CurrentUserResponseModel,
)
async def current_user(user: Annotated[UserAlchemy, Depends(check_authorization)]):
    """
    Создана для получения данных о текущем пользователе (необходима авторизация).
    """
    user_model = CurrentUserResponseModel(
        first_name=user.first_name,
        last_name=user.last_name,
        other_name=user.other_name,
        email=user.email,
        phone=user.phone,
        birthday=user.birthday,
        is_admin=user.is_admin,
    )
    return user_model


@router.patch(
    "/current",
    summary="Изменение данных пользователя",
    responses=responses.USERS_EDIT,
    response_model=UpdateUserResponseModel,
)
async def edit_user(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    edit_data: Annotated[UpdateUserModel, Body()],
):
    """
    Создана для изменения данных текущего пользователя (необходима авторизация).
    """

    if edit_data.first_name:
        user.first_name = edit_data.first_name

    if edit_data.last_name:
        user.last_name = edit_data.last_name

    if edit_data.other_name:
        user.other_name = edit_data.other_name

    if edit_data.email:
        if not await email_validation(edit_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
            )
        user.email = edit_data.email

    if edit_data.phone:
        user.phone = edit_data.phone

    if edit_data.birthday:
        if not await iso_date_validation(edit_data.birthday):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format (ISO required)",
            )
        user.birthday = edit_data.birthday

    await queries_users.update_user_public(user.id, edit_data)
    user_model = UpdateUserResponseModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        other_name=user.other_name,
        email=user.email,
        phone=user.phone,
        birthday=user.birthday,
    )

    return user_model


@router.get(
    "",
    summary="Постраничное получение кратких данных обо всех пользователях",
    responses=responses.USERS,
    response_model=UsersListResponseModel,
)
async def users(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    page: Annotated[int, Query(gt=0)],
    size: Annotated[int, Query(gt=0)],
):
    """
    Создана для постраничного просмотра пользователей (необходима авторизация).
    """
    my_data = await queries_users.get_users(page, size)
    users_list = []
    for user in my_data["users"]:
        add_user = UsersListElementModel(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
        )
        users_list.append(add_user)

    pagination = PaginatedMetaDataModel(total=my_data["total"], page=page, size=size)
    meta = UsersListMetaDataModel(pagination=pagination)

    result = UsersListResponseModel(data=users_list, meta=meta)

    return result
