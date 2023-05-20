from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import desc

from .core import get_session
from .core import UserAlchemy

from ..api.models import PrivateUpdateUserModel
from ..api.models import UpdateUserModel


async def check_in_table(email: str) -> bool:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy).where(UserAlchemy.email == email)
        )
        db_user = result.scalar()

        if not db_user:
            return False

        return True


async def check_in_table_by_id(user_id: int) -> bool:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy).where(UserAlchemy.id == user_id)
        )
        db_user = result.scalar()

        if not db_user:
            return False

        return True


async def get_password_hash(email: str) -> str:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy.password_hash).where(UserAlchemy.email == email)
        )
        return result.first()[0]


async def get_user_by_email(email: str) -> UserAlchemy:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy).where(UserAlchemy.email == email)
        )
        return result.scalar()


async def get_user_by_temp_token(token: str) -> UserAlchemy:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy).where(UserAlchemy.temp_token == token)
        )
        return result.scalar()


async def get_user_by_id(user_id: int) -> UserAlchemy:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy).where(UserAlchemy.id == user_id)
        )
        return result.scalar()


async def set_temp_token(email: str, token: str) -> None:
    async with await get_session() as session:
        query = (
            update(UserAlchemy)
            .where(UserAlchemy.email == email)
            .values(temp_token=token)
        )
        await session.execute(query)
        await session.commit()


async def update_user_public(user_id: int, edit_data: UpdateUserModel) -> None:
    async with await get_session() as session:
        if edit_data.first_name:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(first_name=edit_data.first_name)
            )
            await session.execute(query)

        if edit_data.last_name:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(last_name=edit_data.last_name)
            )
            await session.execute(query)

        if edit_data.other_name:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(other_name=edit_data.other_name)
            )
            await session.execute(query)

        if edit_data.email:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(email=edit_data.email)
            )
            await session.execute(query)

        if edit_data.phone:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(phone=edit_data.phone)
            )
            await session.execute(query)

        if edit_data.birthday:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(birthday=edit_data.birthday)
            )
            await session.execute(query)

        await session.commit()


async def update_user(user_id: int, edit_data: PrivateUpdateUserModel) -> None:
    async with await get_session() as session:
        if edit_data.first_name:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(first_name=edit_data.first_name)
            )
            await session.execute(query)

        if edit_data.last_name:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(last_name=edit_data.last_name)
            )
            await session.execute(query)

        if edit_data.other_name:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(other_name=edit_data.other_name)
            )
            await session.execute(query)

        if edit_data.email:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(email=edit_data.email)
            )
            await session.execute(query)

        if edit_data.phone:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(phone=edit_data.phone)
            )
            await session.execute(query)

        if edit_data.birthday:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(birthday=edit_data.birthday)
            )
            await session.execute(query)

        if edit_data.is_admin:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(is_admin=edit_data.is_admin)
            )
            await session.execute(query)

        if edit_data.city:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(city=edit_data.city)
            )
            await session.execute(query)

        if edit_data.additional_info:
            query = (
                update(UserAlchemy)
                .where(UserAlchemy.id == user_id)
                .values(additional_info=edit_data.additional_info)
            )
            await session.execute(query)

        await session.commit()


async def get_users(page: int, size: int) -> dict:
    async with await get_session() as session:
        offset = (page - 1) * size
        query = (
            select(UserAlchemy)
            .order_by(desc(UserAlchemy.id))
            .offset(offset)
            .limit(size)
        )
        result = await session.execute(query)
        rows = result.fetchall()
        users = []
        for row in rows:
            user = {
                "id": row.UserAlchemy.id,
                "first_name": row.UserAlchemy.first_name,
                "last_name": row.UserAlchemy.last_name,
                "email": row.UserAlchemy.email,
                "city": row.UserAlchemy.city,
            }
            users.append(user)
        my_data = {"users": users}

        total_users = await session.execute(select(UserAlchemy))
        total_users = len(total_users.all())
        total_pages = total_users // size
        if not total_users % size == 0:
            total_pages += 1

        my_data["total"] = total_pages

        return my_data


async def add_user(user: UserAlchemy) -> None:
    async with await get_session() as session:
        session.add(user)
        await session.commit()


async def delete_user(user_id: int) -> None:
    async with await get_session() as session:
        user = await get_user_by_id(user_id)
        await session.delete(user)
        await session.commit()


async def add_super_user() -> None:
    async with await get_session() as session:
        result = await session.execute(
            select(UserAlchemy).where(UserAlchemy.email == "admin")
        )
        db_user = result.scalar()

        if not db_user:
            p_hash = "$2b$12$8k00ua.6ve5zvuftTXdvbu9CHOFVwA57g1UnLQAfqW/cQkVNLjyVu"
            user = UserAlchemy(
                first_name="Super",
                last_name="User",
                email="admin",
                is_admin=True,
                password_hash=p_hash,
            )
            session.add(user)
            await session.commit()
