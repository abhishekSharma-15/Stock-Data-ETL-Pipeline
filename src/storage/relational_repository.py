import pandas as pd
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

class RelationalRepository:

    def __init__(
        self,
        engine: AsyncEngine
    ):
        self.engine = engine

    async def get_last_date(
        self,
        symbol: str
    ) -> datetime | None:
        
        query = text("""
            SELECT MAX(dp.date)
            FROM daily_prices AS dp
            INNER JOIN stocks AS s 
                ON s.stock_id = dp.stock_id
            WHERE s.symbol = :symbol
        """)

        async with self.engine.connect() as conn:
            result = await conn.execute(
                query,
                {'symbol': symbol}
            )
            
        return result.scalar_one()

    # def upsert_stock(self, symbol: str) -> int:

    #     query = """
    #     INSERT INTO stocks (symbol) 
    #     VALUES (:symbol) 
    #     ON CONFLICT (symbol) DO NOTHING;
    #     """

    #     select_query = """
    #     SELECT stock_id 
    #     FROM stocks 
    #     where symbol = :symbol;
    #     """

    #     with self.engine.begin() as conn:
    #         conn.execute(text(query), {'symbol':symbol})
    #         result = conn.execute(text(select_query), {'symbol':symbol}).fetchone()
        
    #     return result[0]

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