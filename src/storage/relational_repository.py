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

    async def read_lastest_date(
        self,
        symbol: str
    ) -> datetime | None:
        
        query = text("""
            SELECT MAX(dp.date)
            FROM stock_daily_price AS dp
            INNER JOIN stock_info AS s 
                ON s.stock_id = dp.stock_id
            WHERE s.symbol = :symbol
        """)

        async with self.engine.connect() as conn:
            result = await conn.execute(
                query,
                {'symbol': symbol}
            )
            
        return result.scalar_one()

    async def create_stock_info(
        self,
        symbol: str,
        company_name: str,
        exchange: str
    ) -> int:
        
        insert_query = text("""
            INSERT INTO stock_info (
                symbol, 
                company_name,
                exchange
            )
            VALUES (
                :symbol,
                :company_name,
                :exchange
            )
            ON CONFLICT (symbol, company_name, exchange DO NOTHING)
            RETURNING stock_id;
        """)

        async with self.engine.begin() as conn:
            result = await conn.execute(
                insert_query,
                {
                    'symbol': symbol,
                    'company_name': company_name,
                    'exchange': exchange
                }
            )

            stock_id = result.scalar_one_or_none()
            if stock_id is not None:
                return stock_id

            result = await conn.execute(
                text("""
                    SELECT stock_id
                    FROM stock_info
                    WHERE symbol = :symbol;
                """),
                {"symbol": symbol},
            )

            return result.scalar_one()

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