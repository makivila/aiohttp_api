import datetime
import uuid
from sqlalchemy import insert, select, update
from app.models.models import Session, sessions_table, users_table, roles_table
from sqlalchemy.ext.asyncio.engine import AsyncEngine


class SessionManager:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def get_session_by_id(self, session_id: str) -> Session:
        async with self._engine.connect() as db_session:
            stmt = (
                select(
                    sessions_table.c.last_activity,
                    users_table.c.id.label("user_id"),
                    roles_table.c.role,
                    roles_table.c.permissions,
                )
                .select_from(sessions_table.join(users_table).join(roles_table))
                .where(sessions_table.c.id == session_id)
            )
            result = await db_session.execute(stmt)
            session_row = result.fetchone()

            if not session_row:
                return None

            return Session(
                id=session_id,
                user_id=session_row.user_id,
                last_activity=session_row.last_activity,
                role=session_row.role,
                permissions=session_row.permissions,
            )

    async def set_session(self, user_id: int) -> str:
        async with self._engine.begin() as db_session:
            stmt = select(sessions_table).where(sessions_table.c.user_id == user_id)
            result = await db_session.execute(stmt)
            session_row = result.fetchone()

            new_session_id = str(uuid.uuid4())

            if session_row:
                stmt = (
                    update(sessions_table)
                    .where(sessions_table.c.id == session_row.id)
                    .values(
                        {
                            sessions_table.c.id: new_session_id,
                            sessions_table.c.last_activity: datetime.datetime.now(),
                        }
                    )
                )

                await db_session.execute(stmt)
            else:
                stmt = insert(sessions_table).values(
                    id=new_session_id,
                    user_id=user_id,
                    last_activity=datetime.datetime.now(),
                )

                await db_session.execute(stmt)

            return new_session_id
