from sqlalchemy import create_engine, Engine
from src.utils.config import DATABASE_URL

def create_database_engine() -> Engine:
    return create_engine(
        url=DATABASE_URL,
        pool_pre_ping=True,
    )
