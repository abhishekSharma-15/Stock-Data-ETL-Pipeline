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
    logger = get_logger("Stock Price Pipeline")

    try:
        engine = create_database_engine()
        await init_db(engine)
        logger.info("Relational database initialized")

        client = create_object_storage_client()
        configure_versioning(client)
        logger.info("Object storage initialized")

        relational_repository = RelationalRepository(engine=engine)
        object_repository = ObjectRepository(client=client)
        orchestrator = StockOrchestrator(
            logger=logger,
            relational_repository=relational_repository,
            object_repository=object_repository,
            symbols=STOCK_SYMBOLS,
        )

        await orchestrator.run()

    except Exception as e:
        logger.exception("Stock Price Pipeline failed %s", e)
        raise


if __name__ == "__main__":
    asyncio.run(main())