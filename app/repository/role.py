from typing import List
from sqlalchemy import delete, select, update
from app.models.models import Role
from database.database import get_db_session


class RoleRepository:
    async def create_role(self, role: Role) -> None:
        async with get_db_session() as session:
            async with session.begin():
                session.add(role)

        return role

    async def get_role_by_role_name(self, role_name: str) -> Role:
        async with get_db_session() as session:
            stmt = select(Role).where(Role.role == role_name)
            result = await session.execute(stmt)
            role = result.scalar_one_or_none()

        return role

    async def get_role_by_id(self, id: int) -> Role:
        async with get_db_session() as session:
            stmt = select(Role).where(Role.id == id)
            result = await session.execute(stmt)
            role = result.scalar_one_or_none()

        return role

    async def get_all_roles(self) -> List[Role]:
        async with get_db_session() as session:
            stmt = select(Role)
            result = await session.execute(stmt)
            roles = result.scalars()

        return roles

    async def update_role(self, role: Role) -> None:
        async with get_db_session() as session:
            async with session.begin():
                stmt = (
                    update(Role)
                    .where(Role.id == role.id)
                    .values(
                        {
                            Role.role: role.role,
                            Role.permissions: role.permissions,
                        }
                    )
                )

                await session.execute(stmt)

    async def delete_role(self, id: int) -> None:
        async with get_db_session() as session:
            async with session.begin():
                stmt = delete(Role).where(Role.id == id)
                await session.execute(stmt)
