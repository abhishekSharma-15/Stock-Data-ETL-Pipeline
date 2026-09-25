from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import TypedDict


class RawStockPrice(TypedDict):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass
class ExtractorResult:
    meta: dict[str, str]
    data: list[RawStockPrice]


@dataclass
class StockMetaData:
    symbol: str
    company_name: str
    exchange: str


@dataclass
class StockPriceData:
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class PipelineStatus(Enum):
    SUCCESS = "success"
    RATE_LIMITED = "rate_limited"
    NO_DATA = "no_data"
    FAILED = "failed"


@dataclass
class PipelineResult:
    symbol: str
    status: PipelineStatus
    error: Exception | None = None
