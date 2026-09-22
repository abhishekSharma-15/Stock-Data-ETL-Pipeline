import numpy as np
import pandas as pd
from logging import Logger

from src.utils.models import StockPrice

def transform(
    logger: Logger,
    data: list[StockPrice],
) -> pd.DataFrame:

    if not data:
        logger.warning('No data provided to Transformer')
        return pd.DataFrame()

    df = pd.DataFrame([
        {
            "date": price.date,
            "open": price.open,
            "high": price.high,
            "low": price.low,
            "close": price.close,
            "volume": price.volume,
        }
        for price in data
    ])

    # 1. Data quality / ordering
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = (
        df
        .sort_values("date")
        .drop_duplicates(subset="date", keep="last")
        .reset_index(drop=True)
    )

    # Ensure numerical columns have the expected type
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # 2. Price-based returns
    df["daily_return"] = df["close"].pct_change()
    df["log_return"] = np.log(
        df["close"] / df["close"].shift(1)
    )

    # 3. Intraday price features
    df["intraday_range"] = (
        (df["high"] - df["low"])
        / df["open"]
    )
    df["intraday_return"] = (
        (df["close"] - df["open"])
        / df["open"]
    )

    # 4. Moving averages
    df["ma_20d"] = (
        df["close"]
        .rolling(window=20, min_periods=20)
        .mean()
    )
    df["ma_50d"] = (
        df["close"]
        .rolling(window=50, min_periods=50)
        .mean()
    )

    # 5. Rolling volatility
    df["volatility_20d"] = (
        df["log_return"]
        .rolling(window=20, min_periods=20)
        .std()
    )
    df["volatility_20d_annualized"] = (
        df["volatility_20d"] * np.sqrt(252)
    )

    # 6. Rolling price statistics
    df["rolling_high_20d"] = (
        df["high"]
        .rolling(window=20, min_periods=20)
        .max()
    )
    df["rolling_low_20d"] = (
        df["low"]
        .rolling(window=20, min_periods=20)
        .min()
    )

    # 8. Volume features
    df["volume_ma_20d"] = (
        df["volume"]
        .rolling(window=20, min_periods=20)
        .mean()
    )
    df["volume_ratio_20d"] = (
        df["volume"] / df["volume_ma_20d"]
    )

    # 10. Clean impossible values
    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return df