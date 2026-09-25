from datetime import datetime
from logging import Logger

from src.utils.interface import Parser
from src.utils.models import RawStockPrice, StockMetaData, StockPriceData


class StockParser(Parser):
    def __init__(
        self,
        logger: Logger,
    ):
        self.logger = logger

    def parse_meta(self, symbol: str, data: dict[str, str]) -> StockMetaData:

        return StockMetaData(
            symbol=symbol, company_name=data["name"], exchange=data["exchangeCode"]
        )

    def parse_data(self, data: list[RawStockPrice]) -> list[StockPriceData]:
        return [
            StockPriceData(
                date=datetime.fromisoformat(prices["date"].replace("Z", "+00:00")),
                open=float(prices["open"]),
                high=float(prices["high"]),
                low=float(prices["low"]),
                close=float(prices["close"]),
                volume=int(prices["volume"]),
            )
            for prices in data
        ]
