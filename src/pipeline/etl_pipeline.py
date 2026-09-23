import aiohttp
import asyncio
from logging import Logger
from datetime import date, datetime
from src.utils.config import START_DATE
from src.utils.models import ExtractorResult, RawStockPrice
from src.transformation.stock_transformer import transform
from src.utils.models import ETLDependencies

class StockETLPipeline:

    def __init__(
        self,
        logger: Logger,
        symbol: str,
        dependencies: ETLDependencies
    ):    
        self.logger = logger
        self.symbol = symbol
        self.relational_repository = dependencies.relational_storage
        self.object_repository = dependencies.object_storage
        self.extractor = dependencies.extractor
        self.parser = dependencies.parser
        self.start_date = START_DATE

    async def _extract(self, start_date: date) -> ExtractorResult | Exception:
        return await self.extractor.extract(
            symbol=self.symbol,
            from_date=start_date,
        )

    async def _store_meta_data(
        self,
        payload: dict[str, str],
    ) -> None:

        object_name = f"meta/{self.symbol}.json"
        await self.object_repository.upload_object(
            object_name=object_name,
            payload=payload
        )

    async def _store_raw_data(
        self,
        payload: list[RawStockPrice],
        start_date: datetime,
        last_update_date: datetime | None = None,
    ) -> None:

        if last_update_date is None:
            object_name = f"historical/{self.symbol}.json"
        else:
            object_name = (
                f"daily/{start_date}/{self.symbol}.json"
            )

        await self.object_repository.upload_object(
            object_name=object_name,
            payload=payload,
        )

    async def run(self) -> None:
        try:
            last_update_date = await self.relational_repository.read_lastest_date(symbol=self.symbol)
            start_date = self.start_date if last_update_date is None else last_update_date

            raw_data = await self._extract(start_date)
            if not raw_data or isinstance(raw_data,Exception):
                self.logger.warning("No data returned for %s",self.symbol,)
                return

            await self._store_meta_data(payload=raw_data.meta)
            await self._store_raw_data(
                payload=raw_data.data,
                start_date=start_date,
                last_update_date=last_update_date,
            )

            parsed_meta = self.parser.parse_meta(symbol=self.symbol, data=raw_data.meta) 
            parsed_data = self.parser.parse_data(data=raw_data.data)
            
            transformed_data = transform(logger=self.logger, data=parsed_data)

            stock_id = await self.relational_repository.read_lastest_date(self.symbol)

        except (aiohttp.ClientError, TimeoutError) as exec:
            self.logger.error("Failed to fetch data for %s: %s", self.symbol, exec)
            return 

        except Exception as exc:
            self.logger.exception("Unexpected error during fetch for %s: %s", self.symbol, exc)
            return

        if not raw_data:
            self.logger.warning("No data returned for %s, skipping storage.", self.symbol)
            return


        # try:
        #     stock_id  = self.dependencies.loader.upsert_stock(self.symbol)
        #     self.dependencies.loader.load_daily_prices(df_features, stock_id)

        # except OperationalError as e:
        #     self.logger.error(f'Database Connection Error: {e}')
        #     raise 
        
        # except IntegrityError as e:
        #     self.logger.error(f'No Data Found: {e}')
        #     raise
        
        # except Exception as err:
        #     self.logger.error(f'Unexpected Python Error: {err}', exc_info=True)
        #     raise

        # self.logger.info(f'ETL pipeline completed for {self.symbol}')