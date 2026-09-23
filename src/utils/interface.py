import pandas as pd
from datetime import date
from abc import ABC, abstractmethod
from typing import Protocol, Any
from src.utils.models import ExtractorResult, StockMetaData, StockPriceData, RawStockPrice

class Extractor(Protocol):

    async def extract(
        self,
        symbol: str,
        from_date: date | None = None,
        to_date: date | None = None
    ) -> ExtractorResult:
        ...

class Parser(Protocol):

    def parse_meta(self, symbol: str, data: dict[str, str]) -> StockMetaData:
        ...

    def parse_data(self, data: list[RawStockPrice]) -> list[StockPriceData]:
        ...

class Transformer(Protocol):

    def transform(self, data: list[StockPriceData]) -> pd.DataFrame:
        ...

class RelationalRepo(Protocol):

    async def get_latest_date(self, symbol: str) -> date | None:
        ...

    async def insert_stock_info(self, data: StockMetaData) -> Any | None:
        ...

    async def upsert_daily_prices(self, stock_id: int, data: pd.DataFrame) -> None:
        ...

class ObjectRepo(Protocol):

    async def upload_object(self, object_name: str, payload: dict | list) -> None:
        ...
    
class FeatureCalculator(ABC):
    
    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        ...