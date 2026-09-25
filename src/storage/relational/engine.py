from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.utils.config import DATABASE_URL


def create_database_engine() -> AsyncEngine:
    return create_async_engine(
        url=DATABASE_URL,
        pool_pre_ping=True,
    )
