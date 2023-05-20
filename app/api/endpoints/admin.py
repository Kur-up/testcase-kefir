from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from . import responses

from .dependencies import check_authorization
from .dependencies import email_validation
from .dependencies import iso_date_validation
from .dependencies import create_password_hash

from ..models import UsersListElementModel
from ..models import PaginatedMetaDataModel

from ..models import PrivateUsersListResponseModel
from ..models import PrivateUsersListMetaDataModel
from ..models import PrivateUsersListHintMetaModel
from ..models import CitiesHintModel
from ..models import PrivateCreateUserModel
from ..models import PrivateDetailUserResponseModel
from ..models import PrivateUpdateUserModel

from ...db import queries_users
from ...db import queries_cities
from ...db.core import UserAlchemy

router = APIRouter(tags=["admin"])


@router.get(
    "/users",
    summary="Постраничное получение кратких данных обо всех пользователях",
    responses=responses.PRIVATE_USERS,
    response_model=PrivateUsersListResponseModel,
)
async def private_users(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    page: Annotated[int, Query(gt=0)],
    size: Annotated[int, Query(gt=0)],
):
    """
    Создана для постраничного просмотра пользователей (необходима авторизация и права администратора).
    """

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You need to be an admin"
        )

    my_data = await queries_users.get_users(page, size)
    users = []
    cities = []
    for user in my_data["users"]:
        add_user = UsersListElementModel(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
        )
        if user["city"]:
            city_name = await queries_cities.get_city_name_by_id(user["city"])
            add_city = CitiesHintModel(id=user["id"], name=city_name)
            cities.append(add_city)

        users.append(add_user)

    pagination = PaginatedMetaDataModel(total=my_data["total"], page=page, size=size)

    hint = PrivateUsersListHintMetaModel(city=cities)
    meta = PrivateUsersListMetaDataModel(pagination=pagination, hint=hint)

    result = PrivateUsersListResponseModel(data=users, meta=meta)

    return result


@router.post(
    "/users",
    summary="Создание пользователя",
    responses=responses.PRIVATE_USERS_POST,
    response_model=PrivateDetailUserResponseModel,
    status_code=201,
)
async def private_create_users(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    create_data: Annotated[PrivateCreateUserModel, Body()],
):
    """
    Создана для создания пользователей (необходима авторизация и права администратора).
    """

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You need to be an admin"
        )

    if not await email_validation(create_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
        )

    if await queries_users.check_in_table(create_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use by another user",
        )

    if create_data.birthday:
        if not await iso_date_validation(create_data.birthday):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format (ISO required)",
            )

    if create_data.city:
        if not await queries_cities.check_city_in_table(create_data.city):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid city id, not found",
            )

    password_hash = await create_password_hash(create_data.password)

    new_user = UserAlchemy(
        first_name=create_data.first_name,
        last_name=create_data.last_name,
        other_name=create_data.other_name,
        email=create_data.email,
        phone=create_data.phone,
        birthday=create_data.birthday,
        city=create_data.city,
        additional_info=create_data.additional_info,
        is_admin=create_data.is_admin,
        password_hash=password_hash,
    )

    await queries_users.add_user(new_user)

    result = PrivateDetailUserResponseModel(
        id=user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        other_name=new_user.other_name,
        email=new_user.email,
        phone=new_user.phone,
        birthday=new_user.birthday,
        is_admin=new_user.is_admin,
        city=new_user.city,
        additional_info=new_user.additional_info,
    )
    result = jsonable_encoder(result)

    return JSONResponse(status_code=201, content=result)


@router.get(
    "/users/{pk}",
    summary="Детальное получение информации о пользователе",
    responses=responses.PRIVATE_USERS_PK,
    response_model=PrivateDetailUserResponseModel,
)
async def private_get_user(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    pk: Annotated[int, Path()],
):
    """
    Создана для получения информации о конкретном пользователе (необходима авторизация и права администратора).
    """

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You need to be an admin"
        )

    if not await queries_users.check_in_table_by_id(pk):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    find_user = await queries_users.get_user_by_id(pk)
    result = PrivateDetailUserResponseModel(
        id=user.id,
        first_name=find_user.first_name,
        last_name=find_user.last_name,
        other_name=find_user.other_name,
        email=find_user.email,
        phone=find_user.phone,
        birthday=find_user.birthday,
        is_admin=find_user.is_admin,
        city=find_user.city,
        additional_info=find_user.additional_info,
    )

    return result


@router.delete(
    "/users/{pk}",
    summary="Удаление пользователя",
    responses=responses.PRIVATE_DELETE,
    status_code=204,
)
async def private_delete_user(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    pk: Annotated[int, Path()],
):
    """
    Создана для удаления информации о конкретном пользователе (необходима авторизация и права администратора).
    """

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You need to be an admin"
        )

    if not await queries_users.check_in_table_by_id(pk):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await queries_users.delete_user(pk)
    return {}


@router.patch(
    "/users/{pk}",
    summary="Изменение информации о пользователе",
    responses=responses.PRIVATE_UPDATE,
    response_model=PrivateDetailUserResponseModel,
)
async def private_patch_user(
    user: Annotated[UserAlchemy, Depends(check_authorization)],
    pk: Annotated[int, Path()],
    edit_data: Annotated[PrivateUpdateUserModel, Body()],
):
    """
    Создана для изменения информации о пользователе конкретном пользователе (необходима авторизация и права администратора).
    """

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You need to be an admin"
        )

    if not await queries_users.check_in_table_by_id(pk):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if edit_data.email:
        if not await email_validation(edit_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
            )

    if edit_data.birthday:
        if not await iso_date_validation(edit_data.birthday):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format (ISO required)",
            )
        user.birthday = edit_data.birthday

    if edit_data.city:
        if not await queries_cities.check_city_in_table(edit_data.city):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid city id, not found",
            )

    await queries_users.update_user(pk, edit_data)
    updated_user = await queries_users.get_user_by_id(pk)
    result = PrivateDetailUserResponseModel(
        id=updated_user.id,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        other_name=updated_user.other_name,
        email=updated_user.email,
        phone=updated_user.phone,
        birthday=updated_user.birthday,
        is_admin=updated_user.is_admin,
        city=updated_user.city,
        additional_info=updated_user.additional_info,
    )

    return result
