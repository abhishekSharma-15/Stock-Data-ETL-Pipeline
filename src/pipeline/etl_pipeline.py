import aiohttp
from logging import Logger
from src.utils.config import START_DATE
from src.ingestion.stock_fetcher import fetch
from src.transformation.stock_parser import parse
from src.transformation.stock_transformer import transform
from src.storage.relational_repository import RelationalRepository
from src.storage.object_repository import ObjectRepository

class StockETLPipeline:

    def __init__(
        self,
        logger: Logger,
        symbol: str,
        relational_repository: RelationalRepository,
        object_repository: ObjectRepository,
        session: aiohttp.ClientSession
    ):    
        self.logger = logger
        self.symbol = symbol
        self.relational_repository = relational_repository
        self.object_repository = object_repository
        self.session = session
        self.start_date = START_DATE

    async def run(self) -> None:

        last_update_date = await self.relational_repository.get_last_date(symbol=self.symbol)
        start_date = self.start_date if last_update_date is None else last_update_date
        
        try:
            raw_data = await fetch(
                logger=self.logger,
                symbol=self.symbol,
                session=self.session,
                start_date=start_date,
            )

        except (aiohttp.ClientError, TimeoutError) as exec:
            self.logger.error("Failed to fetch data for %s: %s", self.symbol, exec)
            return 

        except Exception as exc:
            self.logger.exception("Unexpected error during fetch for %s: %s", self.symbol, exc)
            return

        if not raw_data:
            self.logger.warning("No data returned for %s, skipping storage.", self.symbol)
            return

        if last_update_date is None:
            object_name = f'historical/{self.symbol}'
        else:
            object_name = f'daily/{start_date.date()}/{self.symbol}'

        await self.object_repository.upload_object(
            object_name=object_name,
            payload=raw_data
        )

        # ? raw_data is dict but gives exception to, data: dict[str, Any]
        parsed_data = parse(logger=self.logger, symbol=self.symbol, data=raw_data) # type: ignore

        transformed_data = transform(logger=self.logger, data=parsed_data)
        
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