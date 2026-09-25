import asyncio

import aiohttp

from src.extract.stock_extractor import StockExtractor
from src.orchestration.orchestrator import StockOrchestrator
from src.storage.object.bucket import configure_versioning
from src.storage.object.client import create_minio_client
from src.storage.object.repository import ObjectRepository
from src.storage.relational.engine import create_database_engine
from src.storage.relational.init_db import init_db
from src.storage.relational.operations.executor import SQLExecutor
from src.storage.relational.repository import RelationalRepository
from src.transformation.stock_parser import StockParser
from src.transformation.stock_transformer import StockTransformer
from src.utils.config import MAX_CONCURRENCY, MINIO_BUCKET, STOCK_SYMBOLS
from src.utils.logger import get_logger


async def main():
    logger = get_logger("Stock Price Pipeline")

    try:
        engine = create_database_engine()
        await init_db(engine)
        logger.info("Relational database initialized")

        client = create_minio_client()
        configure_versioning(client=client, bucket=MINIO_BUCKET)
        logger.info("Object storage initialized")

        semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

        async with aiohttp.ClientSession() as session:
            extractor = StockExtractor(
                logger=logger,
                session=session,
                semaphore=semaphore,
            )
            parser = StockParser(logger=logger)
            transformer = StockTransformer(logger=logger)
            executor = SQLExecutor(engine=engine)
            relational_repository = RelationalRepository(executor=executor)
            object_repository = ObjectRepository(client=client)

            orchestrator = StockOrchestrator(
                logger=logger,
                symbols=STOCK_SYMBOLS,
                extractor=extractor,
                parser=parser,
                transformer=transformer,
                relational_storage=relational_repository,
                object_storage=object_repository,
            )

            await orchestrator.run()

    except Exception:
        logger.exception("Stock Price Pipeline failed")
        raise


if __name__ == "__main__":
    asyncio.run(main())
