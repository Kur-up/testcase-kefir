import datetime
import hashlib
import re
from typing import Annotated
from typing import Any

from fastapi import Request
from fastapi import HTTPException
from fastapi import status

from passlib.context import CryptContext

from ...db import queries_users
from ...db.core import UserAlchemy


async def check_password(email: str, password: str) -> bool:
    hasher = CryptContext(schemes=["bcrypt"])
    user_password_hash = await queries_users.get_password_hash(email)
    return hasher.verify(password, user_password_hash)


async def create_password_hash(password: str) -> str:
    hasher = CryptContext(schemes=["bcrypt"])
    hashed_password = hasher.hash(password)
    return hashed_password


async def create_temp_token(email: str) -> str:
    current_datetime = datetime.datetime.now()
    timestamp = int(current_datetime.timestamp())
    salt = "JUST-MY-SALT-FOR-EXAMPLE"
    not_hashed = f"{salt}{email}{timestamp}"
    hashed_token = hashlib.sha256(not_hashed.encode()).hexdigest()
    await queries_users.set_temp_token(email, hashed_token)
    return hashed_token


async def check_authorization(request: Request) -> UserAlchemy:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await queries_users.get_user_by_temp_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


async def email_validation(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


async def iso_date_validation(birthday: str) -> bool:
    try:
        datetime.datetime.fromisoformat(str(birthday))
        return True
    except ValueError:
        return False
