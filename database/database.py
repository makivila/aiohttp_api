from sqlalchemy.ext.asyncio import create_async_engine

from config.config import Config

connection_str = (
    f"postgresql+asyncpg://{Config.DB_USERNAME}:{Config.DB_PASSWORD}"
    + f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_DATABASE_NAME}"
)

engine = create_async_engine(connection_str)
