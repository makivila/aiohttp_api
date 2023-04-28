from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config.config import Config

connection_str = (
    f"postgresql+asyncpg://{Config.DB_USERNAME}:{Config.DB_PASSWORD}"
    + f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_DATABASE_NAME}"
)

engine = create_async_engine(connection_str)


def async_session_generator():
    return sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def get_db_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
