import asyncio
from logging import Logger
from src.utils.models import ETLDependencies
from src.pipeline.etl_pipeline import StockETLPipeline

class StockOrchestrator:

    def __init__(
        self,
        logger: Logger,
        symbols: list[str],
        dependencies: ETLDependencies,
    ):
        self.logger = logger
        self.symbols = symbols
        self.dependencies = dependencies

    async def run(self):
        tasks = [
            StockETLPipeline(
                logger=self.logger,
                symbol=symbol,
                dependencies=self.dependencies
            ).run()
            for symbol in self.symbols
        ]
        await asyncio.gather(*tasks)

        self.logger.info(f'Completed Ingestion for {self.symbols}')