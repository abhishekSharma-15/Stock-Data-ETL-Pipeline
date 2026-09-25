GET_LATEST_DATE = """
    SELECT MAX(dp.date)
    FROM stock_daily_price AS dp
    INNER JOIN stock_info AS s
        ON s.stock_id = dp.stock_id
    WHERE s.symbol = :symbol;
"""

INSERT_STOCK_PRICES = """
    INSERT INTO stock_daily_price (
        stock_id,
        date,
        open,
        high,
        low,
        close,
        volume,
        daily_return,
        log_return,
        intraday_range,
        intraday_return,
        ma_20d,
        ma_50d,
        volatility_20d,
        volatility_20d_annualized,
        volume_ma_20d,
        volume_ratio_50d,
    )
    VALUES (
        stock_id,
        date,
        open,
        high,
        low,
        close,
        volume,
        daily_return,
        log_return,
        ma_20d,
        ma_50d,
        volatility_20d,
        volatility_20d_annualized,
        volume_ma_20d,
        volume_ratio_50d,
    )
"""
