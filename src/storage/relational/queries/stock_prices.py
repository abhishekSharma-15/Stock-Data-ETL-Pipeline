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
        ma_20d,
        ma_50d,
        volatility_20d,
        volatility_20d_annualized,
        volume_ma_20d,
        volume_ratio_50d
    )
    VALUES (
        :stock_id,
        :date,
        :open,
        :high,
        :low,
        :close,
        :volume,
        :daily_return,
        :log_return,
        :ma_20d,
        :ma_50d,
        :volatility_20d,
        :volatility_20d_annualized,
        :volume_ma_20d,
        :volume_ratio_50d
    )
    ON CONFLICT (stock_id, date)
    DO UPDATE SET
        open = EXCLUDED.open,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        close = EXCLUDED.close,
        volume = EXCLUDED.volume,
        daily_return = EXCLUDED.daily_return,
        log_return = EXCLUDED.log_return,
        ma_20d = EXCLUDED.ma_20d,
        ma_50d = EXCLUDED.ma_50d,
        volatility_20d = EXCLUDED.volatility_20d,
        volatility_20d_annualized = EXCLUDED.volatility_20d_annualized,
        volume_ma_20d = EXCLUDED.volume_ma_20d,
        volume_ratio_50d = EXCLUDED.volume_ratio_50d;
"""
