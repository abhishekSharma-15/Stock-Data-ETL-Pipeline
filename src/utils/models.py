from dataclasses import dataclass
from datetime import datetime


@dataclass
class StockPrice:
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int