import asyncio
from logging import Logger

from src.pipeline.etl_pipeline import StockETLPipeline
from src.utils.interface import (
    Extractor,
    ObjectRepo,
    Parser,
    RelationalRepo,
    Transformer,
)
from src.utils.models import PipelineStatus


class StockOrchestrator:
    def __init__(
        self,
        logger: Logger,
        symbols: list[str],
        extractor: Extractor,
        parser: Parser,
        transformer: Transformer,
        relational_storage: RelationalRepo,
        object_storage: ObjectRepo,
    ):
        self.logger = logger
        self.symbols = symbols
        self.extractor = extractor
        self.parser = parser
        self.transformer = transformer
        self.relational_storage = relational_storage
        self.object_storage = object_storage

    async def run(self):
        tasks = [
            StockETLPipeline(
                logger=self.logger,
                symbol=symbol,
                extractor=self.extractor,
                parser=self.parser,
                transformer=self.transformer,
                relational_repository=self.relational_storage,
                object_repository=self.object_storage,
            ).run()
            for symbol in self.symbols
        ]
        results = await asyncio.gather(*tasks)

        successful = [
            result for result in results if result.status == PipelineStatus.SUCCESS
        ]

        rate_limited = [
            result for result in results if result.status == PipelineStatus.RATE_LIMITED
        ]

        failed = [
            result for result in results if result.status == PipelineStatus.FAILED
        ]

        self.logger.info(
            "Ingestion completed: %d succeeded, %d rate limited, %d failed",
            len(successful),
            len(rate_limited),
            len(failed),
        )
