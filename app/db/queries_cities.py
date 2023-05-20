from sqlalchemy import select

from .core import get_session
from .core import CityAlchemy


async def get_city_name_by_id(city_id: int) -> str:
    async with await get_session() as session:
        result = await session.execute(
            select(CityAlchemy).where(CityAlchemy.id == city_id)
        )
        city = result.scalar()
        return city.name


async def check_city_in_table(city_id: int) -> bool:
    async with await get_session() as session:
        result = await session.execute(
            select(CityAlchemy).where(CityAlchemy.id == city_id)
        )
        db_city = result.scalar()

        if not db_city:
            return False

        return True


async def add_default_cities() -> None:
    async with await get_session() as session:
        result = await session.execute(
            select(CityAlchemy).where(CityAlchemy.name == "Moscow")
        )
        db_city = result.scalar()
        if not db_city:
            city = CityAlchemy(name='Moscow')
            session.add(city)
            await session.commit()