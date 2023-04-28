from typing import List
from sqlalchemy import delete, insert, select, update
from app.models.models import User, users_table
from sqlalchemy.ext.asyncio.engine import AsyncEngine


class UserRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def get_user_by_login(self, login: str) -> User:
        async with self._engine.connect() as conn:
            stmt = select(users_table).where(users_table.c.login == login)
            result = await conn.execute(stmt)
            user_row = result.fetchone()

            if not user_row:
                return None

            return User(
                id=user_row.id,
                first_name=user_row.first_name,
                second_name=user_row.second_name,
                login=user_row.login,
                password=user_row.password,
                born=user_row.born,
                registration_date=user_row.registration_date,
                role_id=user_row.role_id,
            )

    async def get_user_by_id(self, id: int) -> User:
        async with self._engine.connect() as conn:
            stmt = select(users_table).where(users_table.c.id == id)
            result = await conn.execute(stmt)
            user_row = result.fetchone()

            if not user_row:
                return None

            return User(
                id=user_row.id,
                first_name=user_row.first_name,
                second_name=user_row.second_name,
                login=user_row.login,
                password=user_row.password,
                born=user_row.born,
                registration_date=user_row.registration_date,
                role_id=user_row.role_id,
            )

    async def get_all_users(self) -> List[User]:
        async with self._engine.connect() as conn:
            stmt = select(users_table)
            result = await conn.execute(stmt)
            user_rows = result.fetchall()

            users = []
            for user_row in user_rows:
                users.append(
                    User(
                        id=user_row.id,
                        first_name=user_row.first_name,
                        second_name=user_row.second_name,
                        login=user_row.login,
                        password=user_row.password,
                        born=user_row.born,
                        registration_date=user_row.registration_date,
                        role_id=user_row.role_id,
                    )
                )

            return users

    async def create_user(self, user: User) -> None:
        async with self._engine.begin() as conn:
            stmt = insert(users_table).values(
                first_name=user.first_name,
                second_name=user.second_name,
                login=user.login,
                password=user.password,
                born=user.born,
                registration_date=user.registration_date,
                role_id=user.role_id,
            )
            await conn.execute(stmt)

    async def update_user(self, user: User) -> None:
        async with self._engine.begin() as conn:
            stmt = (
                update(users_table)
                .where(users_table.c.id == user.id)
                .values(
                    {
                        users_table.c.first_name: user.first_name,
                        users_table.c.second_name: user.second_name,
                        users_table.c.login: user.login,
                        users_table.c.password: user.password,
                        users_table.c.born: user.born,
                        users_table.c.role_id: user.role_id,
                    }
                )
            )

            await conn.execute(stmt)

    async def delete_user(self, id: int) -> None:
        async with self._engine.begin() as conn:
            stmt = delete(users_table).where(users_table.c.id == id)
            await conn.execute(stmt)
