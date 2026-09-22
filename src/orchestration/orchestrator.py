import asyncio
import aiohttp
from logging import Logger
from src.storage.relational_repository import RelationalRepository
from src.storage.object_repository import ObjectRepository
from src.pipeline.etl_pipeline import StockETLPipeline

class StockOrchestrator:

    def __init__(
        self,
        logger: Logger,
        relational_repository: RelationalRepository,
        object_repository: ObjectRepository,
        symbols: list[str]
    ):
        self.logger = logger
        self.relational_repository = relational_repository
        self.object_repository = object_repository
        self.symbols = symbols

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                StockETLPipeline(
                    logger=self.logger,
                    symbol=symbol,
                    relational_repository=self.relational_repository,
                    object_repository=self.object_repository,
                    session=session
                ).run()
                for symbol in self.symbols
            ]

            await asyncio.gather(*tasks)

        self.logger.info(f'Completed Ingestion for {self.symbols}')