import asyncio
from datetime import date
from logging import Logger

import aiohttp

from src.utils.config import START_DATE
from src.utils.exceptions import RateLimitError
from src.utils.interface import (
    Extractor,
    ObjectRepo,
    Parser,
    RelationalRepo,
    Transformer,
)
from src.utils.models import (
    ExtractorResult,
    PipelineResult,
    PipelineStatus,
    RawStockPrice,
)


class StockETLPipeline:
    def __init__(
        self,
        logger: Logger,
        symbol: str,
        extractor: Extractor,
        parser: Parser,
        transformer: Transformer,
        relational_repository: RelationalRepo,
        object_repository: ObjectRepo,
    ):
        self.logger = logger
        self.symbol = symbol
        self.extractor = extractor
        self.parser = parser
        self.transformer = transformer
        self.relational_repository = relational_repository
        self.object_repository = object_repository
        self.start_date = START_DATE

    async def _extract(self, start_date: date) -> ExtractorResult:
        return await self.extractor.extract(
            symbol=self.symbol,
            from_date=start_date,
        )

    async def _store_meta_data(self, payload: dict[str, str]) -> None:
        object_name = f"meta/{self.symbol}.json"
        await self.object_repository.upload_object(
            object_name=object_name, payload=payload
        )

    async def _store_raw_data(
        self,
        payload: list[RawStockPrice],
        start_date: str,
        last_update_date: str | None = None,
    ) -> None:

        if last_update_date is None:
            object_name = f"historical/{self.symbol}.json"
        else:
            object_name = f"daily/{start_date}/{self.symbol}.json"

        await self.object_repository.upload_object(
            object_name=object_name,
            payload=payload,
        )

    async def run(self) -> PipelineResult:
        try:
            last_update_date = await self.relational_repository.get_latest_date(
                symbol=self.symbol
            )
            start_date = (
                self.start_date if last_update_date is None else last_update_date
            )

            raw_data = await self._extract(start_date)
            if not raw_data.data:
                self.logger.warning(
                    "No data returned for %s",
                    self.symbol,
                )
                return PipelineResult(symbol=self.symbol, status=PipelineStatus.NO_DATA)

            await asyncio.gather(
                self._store_meta_data(payload=raw_data.meta),
                self._store_raw_data(
                    payload=raw_data.data,
                    start_date=str(start_date),
                    last_update_date=str(last_update_date),
                ),
            )

            parsed_meta = self.parser.parse_meta(symbol=self.symbol, data=raw_data.meta)
            parsed_data = self.parser.parse_data(data=raw_data.data)

            transformed_data = self.transformer.transform(data=parsed_data)
            print(transformed_data.columns)

            stock_id = await self.relational_repository.insert_stock_info(
                data=parsed_meta
            )
            if stock_id is None:
                self.logger.warning(
                    "Could not obtain stock_id for %s",
                    self.symbol,
                )
                return PipelineResult(symbol=self.symbol, status=PipelineStatus.NO_DATA)

            # await self.relational_repository.upsert_daily_prices(data=transformed_data)

            return PipelineResult(
                symbol=self.symbol,
                status=PipelineStatus.SUCCESS,
            )

        except RateLimitError as exec:
            self.logger.error("Failed to fetch data for %s: %s", self.symbol, exec)
            return PipelineResult(
                symbol=self.symbol, status=PipelineStatus.RATE_LIMITED, error=exec
            )

        except (aiohttp.ClientError, TimeoutError) as exec:
            self.logger.error(
                "Network failure while processing %s: %s", self.symbol, exec
            )
            return PipelineResult(
                symbol=self.symbol, status=PipelineStatus.FAILED, error=exec
            )

        except Exception:
            self.logger.exception("Unexpected error during fetch for %s", self.symbol)
            return PipelineResult(symbol=self.symbol, status=PipelineStatus.FAILED)
