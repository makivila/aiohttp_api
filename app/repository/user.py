from typing import List
from sqlalchemy import delete, select, update
from app.models.models import User
from database.database import get_db_session


class UserRepository:
    async def get_user_by_login(self, login: str) -> User:
        async with get_db_session() as session:
            stmt = select(User).where(User.login == login)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

        return user

    async def get_user_by_id(self, id: int) -> User:
        async with get_db_session() as session:
            stmt = select(User).where(User.id == id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

        return user

    async def get_all_users(self) -> List[User]:
        async with get_db_session() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            users = result.scalars()

        return users

    async def create_user(self, user: User) -> None:
        async with get_db_session() as session:
            async with session.begin():
                session.add(user)

    async def update_user(self, user: User) -> None:
        async with get_db_session() as session:
            async with session.begin():
                stmt = (
                    update(User)
                    .where(User.id == user.id)
                    .values(
                        {
                            User.first_name: user.first_name,
                            User.second_name: user.second_name,
                            User.login: user.login,
                            User.password: user.password,
                            User.born: user.born,
                            User.role_id: user.role_id,
                        }
                    )
                )

                await session.execute(stmt)

    async def delete_user(self, id: int) -> None:
        async with get_db_session() as session:
            async with session.begin():
                stmt = delete(User).where(User.id == id)
                await session.execute(stmt)
