import aiohttp
from datetime import datetime
from src.ingestion.stock_fetcher import fetch
from src.storage.stock_repository import StockRepository

class StockETLPipeline:

    def __init__(
        self,
        symbol: str,
        repository: StockRepository,
        session: aiohttp.ClientSession
    ):    
        self.symbol = symbol
        self.repository = repository
        self.session = session

    async def run(self) -> None:

        end_date = self.repository.get_last_date(symbol=self.symbol)


        raw_data = await fetch(
            symbol=self.symbol,
            session=self.session,
            start_date=datetime(2026,1,9),
        )

        
        
        
        # self.fetcher.save_raw_data(raw_data)

        # # Parse
        # df_raw = self.dependencies.parser.parse(raw_data)
        # # self.fetcher.save_csv(df_raw)

        # # Transform   
        # df_clean = self.dependencies.transformer.clean_data(df_raw)
        # df_features = self.dependencies.transformer.add_features(df_clean)
        
            
        # # Load
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