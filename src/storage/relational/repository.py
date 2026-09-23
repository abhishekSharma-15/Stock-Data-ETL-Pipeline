import pandas as pd
from datetime import date
from typing import Any
from src.storage.relational.operations.executor import SQLExecutor
from src.storage.relational.queries.stock_info import INSERT_STOCK_INFO
from src.storage.relational.queries.stock_prices import GET_LATEST_DATE
from src.utils.interface import RelationalRepo
from src.utils.models import StockMetaData

class RelationalRepository(RelationalRepo):

    def __init__(
        self,
        executor: SQLExecutor
    ):
        self.executor = executor

    async def get_latest_date(self, symbol: str,) -> date | None:
        result = await self.executor.fetch_one(
            query=GET_LATEST_DATE,
            params={'symbol': symbol}
        )
        return result[0] if result else None

    async def insert_stock_info(self, data: StockMetaData) -> int | None:
        result = await self.executor.execute_returning_one(
            query=INSERT_STOCK_INFO,
            params={
                'symbol': data.symbol,
                'company_name': data.company_name,
                'exchange': data.exchange
            }
        )
        return result if result else None

    async def upsert_daily_prices(
        self,
        stock_id: int,
        data: pd.DataFrame,
    ) -> None:
        await self.executor.execute(
            query=GET_LATEST_DATE,
            params={
                
            }
        )



    # def load_daily_prices(self, df: pd.DataFrame, stock_id: int):

    #     df = df.copy()
    #     df['stock_id'] = stock_id

    #     df = df[
    #         [
    #             "stock_id", 'date', 'open', 'high', 'low', 'close', 'volume', 
    #             'daily_return', 'log_return', 'volatility_20d', 'ma_20d', 'ma_50d' 
    #         ]
    #     ]

    #     df = df.drop_duplicates(subset=['stock_id','date'])
    #     records = df.to_dict(orient='records')

    #     upsert_query = text ("""
    #         INSERT INTO daily_prices (
    #             stock_id, date, open, high, low, close, volume,
    #             daily_return, log_return, volatility_20d, ma_20d, ma_50d
    #         )
    #         VALUES (
    #             :stock_id, :date, :open, :high, :low, :close, :volume,
    #             :daily_return, :log_return, :volatility_20d, :ma_20d, :ma_50d
    #         )
    #         ON CONFLICT (stock_id, date)
    #         DO UPDATE SET 
    #             open = EXCLUDED.open,
    #             high = EXCLUDED.high,
    #             low = EXCLUDED.low,
    #             close = EXCLUDED.close,
    #             volume = EXCLUDED.volume,
    #             daily_return = EXCLUDED.daily_return,
    #             log_return = EXCLUDED.log_return,
    #             volatility_20d = EXCLUDED.volatility_20d,
    #             ma_20d = EXCLUDED.ma_20d, 
    #             ma_50d = EXCLUDED.ma_50d;
    #     """)

    #     with self.engine.begin() as conn:
    #         conn.execute(upsert_query, records)

    #     self.logger.info(f'Loaded {len(df)} rows into daily_prices')