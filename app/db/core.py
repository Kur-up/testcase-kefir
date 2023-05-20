import os
import datetime

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


async def get_session() -> AsyncSession:
    async_session = AsyncSession(engine, expire_on_commit=False)
    return async_session


class Base(DeclarativeBase):
    pass


class UserAlchemy(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    other_name: Mapped[str] = mapped_column(String(128), default=None, nullable=True)
    email: Mapped[str] = mapped_column(String(256))
    phone: Mapped[str] = mapped_column(String(32), default=None, nullable=True)
    birthday: Mapped[datetime.date] = mapped_column(Date, default=None, nullable=True)
    city: Mapped[int] = mapped_column(Integer, default=None, nullable=True)
    additional_info: Mapped[str] = mapped_column(
        String(512), default=None, nullable=True
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    password_hash: Mapped[str] = mapped_column(String(128))
    temp_token: Mapped[str] = mapped_column(String(256), default=None, nullable=True)


class CityAlchemy(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
