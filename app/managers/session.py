import datetime
import uuid
from sqlalchemy import select, update
from database.database import get_db_session
from app.models.models import Session


class SessionManager:
    async def get_session_by_id(self, session_id: str) -> Session:
        async with get_db_session() as db_session:
            stmt = select(Session).where(Session.id == session_id)
            result = await db_session.execute(stmt)

            session = result.scalar_one_or_none()
            return session

    async def set_session(self, user_id: int) -> str:
        async with get_db_session() as db_session:
            async with db_session.begin():
                stmt = select(Session).where(Session.user_id == user_id)
                result = await db_session.execute(stmt)

                session = result.scalar_one_or_none()

                if session:
                    stmt = (
                        update(Session)
                        .where(Session.id == session.id)
                        .values(
                            {
                                Session.id: str(uuid.uuid4()),
                                Session.last_activity: datetime.datetime.now(),
                            }
                        )
                    )

                    await db_session.execute(stmt)

                else:
                    session = Session(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        last_activity=datetime.datetime.now(),
                    )

                    db_session.add(session)

                return session.id
