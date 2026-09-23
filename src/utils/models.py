from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict
from src.extract.stock_extractor import StockExtractor
from src.transformation.stock_parser import StockParser
from src.storage.relational_repository import RelationalRepository
from src.storage.object_repository import ObjectRepository

@dataclass
class ETLDependencies:
    extractor: StockExtractor
    parser: StockParser
    # transformer: str
    relational_storage: RelationalRepository
    object_storage: ObjectRepository

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
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int