from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

async def init_db(engine: AsyncEngine) -> None:

    create_stock_info_table = text("""
        CREATE TABLE IF NOT EXISTS stock_info (
            stock_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            symbol VARCHAR(20) UNIQUE NOT NULL,
            company_name VARCHAR(50),
            exchange VARCHAR(10)
        );
    """)

    create_stock_daily_price_table = text("""
        CREATE TABLE IF NOT EXISTS stock_daily_price (
            stock_id INTEGER NOT NULL,
            date DATE NOT NULL,

            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume BIGINT,
            
            daily_return FLOAT,
            log_return FLOAT,
            ma_20d FLOAT,
            ma_50d FLOAT,
            volatility_20d FLOAT,
            volatility_20d_annualized FLOAT,
            volume_ma_20d FLOAT,
            volume_ratio_50d FLOAT,

            PRIMARY KEY (stock_id, date),
            
            CONSTRAINT fk_stock
                FOREIGN KEY(stock_id) 
                REFERENCES stock_info(stock_id)
        )
    """)

    async with engine.begin() as conn:
        await conn.execute(create_stock_info_table)
        await conn.execute(create_stock_daily_price_table)