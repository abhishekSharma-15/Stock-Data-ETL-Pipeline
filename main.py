import asyncio
import aiohttp

from src.utils.logger import get_logger
from src.utils.config import STOCK_SYMBOLS, MAX_CONCURRENCY
from src.utils.models import ETLDependencies
from src.extract.stock_extractor import StockExtractor
from src.transformation.stock_parser import StockParser
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

        semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

        async with aiohttp.ClientSession() as session:
            extractor = StockExtractor(
                logger=logger,
                session=session,
                semaphore=semaphore,
            )
            parser = StockParser(logger=logger)
            relational_repository = RelationalRepository(engine=engine)
            object_repository = ObjectRepository(client=client)

            dependencies = ETLDependencies(
                extractor=extractor,
                parser=parser,
                relational_storage=relational_repository,
                object_storage=object_repository
            )
        
            orchestrator = StockOrchestrator(
                logger=logger,
                symbols=STOCK_SYMBOLS,
                dependencies=dependencies,
            )

            await orchestrator.run()

    except Exception as e:
        logger.exception("Stock Price Pipeline failed %s", e)
        raise


if __name__ == "__main__":
    asyncio.run(main())