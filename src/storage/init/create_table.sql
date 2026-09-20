CREATE TABLE IF NOT EXISTS stocks (
    stock_id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_prices (
    stock_id INTEGER NOT NULL,
    date DATE NOT NULL,

    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    daily_return FLOAT,
    log_return FLOAT,
    volatility_20d FLOAT,
    ma_20d FLOAT,
    ma_50d FLOAT,

    PRIMARY KEY (stock_id, date),
    
    CONSTRAINT fk_stock
        FOREIGN KEY(stock_id) 
        REFERENCES stocks(stock_id)
)