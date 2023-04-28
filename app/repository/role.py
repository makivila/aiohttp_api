from typing import List
from sqlalchemy import delete, insert, select, update
from app.models.models import Role, roles_table
from sqlalchemy.ext.asyncio.engine import AsyncEngine


class RoleRepository:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def create_role(self, role: Role) -> None:
        async with self._engine.begin() as conn:
            stmt = insert(roles_table).values(
                role=role.role,
                permissions=role.permissions,
            )

            await conn.execute(stmt)

    async def get_role_by_role_name(self, role_name: str) -> Role:
        async with self._engine.connect() as conn:
            stmt = select(roles_table).where(roles_table.c.role == role_name)
            result = await conn.execute(stmt)
            role_row = result.fetchone()

            if not role_row:
                return None

            return Role(
                id=role_row.id,
                role=role_row.role,
                permissions=role_row.permissions,
            )

    async def get_role_by_id(self, id: int) -> Role:
        async with self._engine.connect() as conn:
            stmt = select(roles_table).where(roles_table.c.id == id)
            result = await conn.execute(stmt)
            role_row = result.fetchone()

            if not role_row:
                return None

            return Role(
                id=role_row.id,
                role=role_row.role,
                permissions=role_row.permissions,
            )

    async def get_all_roles(self) -> List[Role]:
        async with self._engine.connect() as conn:
            stmt = select(roles_table)
            result = await conn.execute(stmt)
            role_rows = result.fetchall()

            roles = []
            for role_row in role_rows:
                roles.append(
                    Role(
                        id=role_row.id,
                        role=role_row.role,
                        permissions=role_row.permissions,
                    )
                )

            return roles

    async def update_role(self, role: Role) -> None:
        async with self._engine.begin() as conn:
            stmt = (
                update(roles_table)
                .where(roles_table.c.id == role.id)
                .values(
                    {
                        roles_table.c.role: role.role,
                        roles_table.c.permissions: role.permissions,
                    }
                )
            )

            await conn.execute(stmt)

    async def delete_role(self, id: int) -> None:
        async with self._engine.begin() as conn:
            stmt = delete(roles_table).where(roles_table.c.id == id)
            await conn.execute(stmt)
