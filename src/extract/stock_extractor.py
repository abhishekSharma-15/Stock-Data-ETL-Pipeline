import asyncio
from datetime import date, datetime
from logging import Logger

import aiohttp
from dateutil import tz
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.utils.config import API_TIMEOUT, START_DATE, TIINGO_API_TOKEN, TIINGO_URL
from src.utils.exceptions import RateLimitError, UnauthorizationCallError
from src.utils.interface import Extractor
from src.utils.models import ExtractorResult, RawStockPrice


class StockExtractor(Extractor):
    def __init__(
        self,
        logger: Logger,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
    ) -> None:
        self.logger = logger
        self.session = session
        self.semaphore = semaphore
        self.url = f"{TIINGO_URL}"

    async def extract(
        self,
        symbol: str,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> ExtractorResult:

        start_date = from_date or START_DATE
        end_date = to_date or datetime.now(tz.tzlocal())

        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()

        meta_url = self.url + f"/{symbol}"
        data_url = self.url + f"/{symbol}/prices"
        headers = {
            "Authorization": f"Token {TIINGO_API_TOKEN}",
            "Content-Type": "application/json",
        }
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
        }

        return ExtractorResult(
            meta=await self._fetch_meta(
                url=meta_url, headers=headers, params=params, symbol=symbol
            ),
            data=await self._fetch_data(
                url=data_url, headers=headers, params=params, symbol=symbol
            ),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception_type(
            (asyncio.TimeoutError, aiohttp.ClientError, RateLimitError)
        ),
        reraise=True,
    )
    async def _fetch_meta(
        self, url: str, params: dict[str, str], headers: dict[str, str], symbol: str
    ) -> dict[str, str]:

        async with self.semaphore, self.session.get(
            url=url,
            headers=headers,
            params=params,
            timeout=aiohttp.ClientTimeout(total=float(API_TIMEOUT)),
        ) as response:
            if response.status == 429:
                self.logger.warning(
                    "Tiingo rate limit hit for %s; retrying with backoff...", symbol
                )
                raise RateLimitError(f"Tiingo rate limit exceeded for {symbol}")

            if response.status in (401, 403):
                self.logger.error(
                    "Unauthorized Tiingo API call (HTTP %s). Check TIINGO_API_TOKEN.",
                    response.status,
                )
                raise UnauthorizationCallError(
                    f"HTTP {response.status}: Invalid or missing API token."
                )

            response.raise_for_status()

            data = await response.json()
            return data

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception_type(
            (asyncio.TimeoutError, aiohttp.ClientError, RateLimitError)
        ),
        reraise=True,
    )
    async def _fetch_data(
        self, url: str, params: dict[str, str], headers: dict[str, str], symbol: str
    ) -> list[RawStockPrice]:

        async with self.semaphore, self.session.get(
            url=url,
            headers=headers,
            params=params,
            timeout=aiohttp.ClientTimeout(total=float(API_TIMEOUT)),
        ) as response:
            if response.status == 429:
                self.logger.warning(
                    "Tiingo rate limit hit for %s; retrying with backoff...", symbol
                )
                raise RateLimitError(f"Tiingo rate limit exceeded for {symbol}")

            if response.status in (401, 403):
                self.logger.error(
                    "Unauthorized Tiingo API call (HTTP %s). Check TIINGO_API_TOKEN.",
                    response.status,
                )
                raise UnauthorizationCallError(
                    f"HTTP {response.status}: Invalid or missing API token."
                )

            response.raise_for_status()

            data: list[RawStockPrice] = await response.json()
            return data
