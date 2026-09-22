import asyncio
from src.utils.logger import get_logger
from src.utils.config import STOCK_SYMBOLS
from src.orchestration.orchestrator import StockOrchestrator
from src.storage.relational_repository import RelationalRepository
from src.storage.object_repository import ObjectRepository
from src.storage.engine import create_database_engine
from src.storage.client import create_object_storage_client
from src.storage.bucket import configure_versioning
from src.storage.init_db import init_db

async def main():
    logger = get_logger('Stock Price Pipeline')

    engine = create_database_engine()
    await init_db(engine)
    client = create_object_storage_client()
    configure_versioning(client)

    relational_repository = RelationalRepository(engine=engine)    
    object_repository = ObjectRepository(client=client)
    orchestrator = StockOrchestrator(
        logger,
        relational_repository,
        object_repository,
        STOCK_SYMBOLS
    )
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(main())
