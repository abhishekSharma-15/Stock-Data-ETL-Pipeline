from typing import Any
import pandas as pd
from datetime import datetime
from logging import Logger
from src.utils.models import StockPrice

def parse(
    logger: Logger,
    symbol: str,
    data: list[dict[str, Any]]
) -> list[StockPrice]:

    return [
        StockPrice(
            date=datetime.fromisoformat(
                prices["date"].replace("Z", "+00:00")
            ),
            open=float(prices["open"]),
            high=float(prices["high"]),
            low=float(prices["low"]),
            close=float(prices["close"]),
            volume=int(prices["volume"]),
        )
        for prices in data
    ]