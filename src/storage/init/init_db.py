from src.storage.engine import create_database_engine
from sqlalchemy import Engine
from sqlalchemy import text
from src.utils.logger import get_logger
from src.utils.config import BASE_DIR

def init_db(engine: Engine):

    with open('src/storage/init/create_table.sql') as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql))