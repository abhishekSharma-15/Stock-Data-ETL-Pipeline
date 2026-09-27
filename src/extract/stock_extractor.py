from datetime import date, datetime
from logging import Logger

from dateutil import tz

from src.utils.config import START_DATE
from src.utils.interface import Extractor, StockDataClient
from src.utils.models import ExtractorResult


class StockExtractor(Extractor):
    def __init__(
        self,
        logger: Logger,
        client: StockDataClient,
    ) -> None:
        self.logger = logger
        self.client = client

    async def extract(
        self,
        symbol: str,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> ExtractorResult:

        start_date = from_date or START_DATE
        end_date = to_date or datetime.now(tz.tzlocal()).date()

        if isinstance(start_date, datetime):
            start_date = start_date.date()

        if isinstance(end_date, datetime):
            end_date = end_date.date()

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        return ExtractorResult(
            meta=await self.client.fetch_meta(
                symbol=symbol,
            ),
            data=await self.client.fetch_data(
                symbol=symbol,
                start_date=start_date_str,
                end_date=end_date_str,
            ),
        )
