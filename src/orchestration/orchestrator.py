import asyncio
import aiohttp
from logging import Logger
from src.utils.models import ETLDependencies
from src.pipeline.etl_pipeline import StockETLPipeline

class StockOrchestrator:

    def __init__(
        self,
        logger: Logger,
        repository,
        symbols: list[str]
    ):
        self.logger = logger
        self.repository = repository
        self.symbols = symbols

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                StockETLPipeline(
                    symbol=symbol,
                    repository=self.repository,
                    session=session
                ).run()
                for symbol in self.symbols
            ]

            await asyncio.gather(*tasks)
        