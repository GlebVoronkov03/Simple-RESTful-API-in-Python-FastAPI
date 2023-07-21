from sqlalchemy import insert, select

from .auth.models import Role
from .db import async_session_maker


async def create_roles():
    async with async_session_maker() as session:
        existing_roles = await session.execute(select(Role))
        if not existing_roles.scalars().first():
            list_roles = [
                {"id": 1, "name": "admin", "permissions": None},
                {"id": 2, "name": "user", "permissions": None},
            ]
            stmt = insert(Role).values(list_roles)
            await session.execute(stmt)
            await session.commit()
