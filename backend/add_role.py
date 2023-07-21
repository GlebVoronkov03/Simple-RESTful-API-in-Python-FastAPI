import asyncio

from sqlalchemy import insert
from src.auth.models import Role
from src.db import async_session_maker


async def create_roles():
    async with async_session_maker() as session:
        list_roles = [
            {"id": 1, "name": "admin", "permissions": None},
            {"id": 2, "name": "user", "permissions": None},
        ]
        stmt = insert(Role).values(list_roles)
        await session.execute(stmt)
        await session.commit()


async def startup():
    await create_roles()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
