import pandas as pd
from datetime import date
from typing import Any, Protocol

RawStockData = dict[str, Any]

class Extractor(Protocol):
    async def extract(
        self,
        symbol: str,
        start_date: date,
    ) -> RawStockData:
        ...

class Parser(Protocol):
    def parse(
        self,
        symbol: str,
        data: RawStockData,
    ) -> pd.DataFrame:
        ...

class Transformer(Protocol):
    def transform(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        ...