import asyncio
from logging import Logger
from typing import Any

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.utils.config import API_TIMEOUT, TIINGO_API_TOKEN, TIINGO_URL
from src.utils.exceptions import (
    RateLimitError,
    UnauthorizationCallError,
)
from src.utils.interface import StockDataClient
from src.utils.models import RawStockPrice


class TiingoClient(StockDataClient):
    def __init__(
        self,
        logger: Logger,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
    ) -> None:

        self.logger = logger
        self.session = session
        self.semaphore = semaphore
        self.base_url = TIINGO_URL
        self.headers = {
            "Authorization": f"Token {TIINGO_API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.timeout = aiohttp.ClientTimeout(total=float(API_TIMEOUT))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception_type(
            (
                asyncio.TimeoutError,
                aiohttp.ClientError,
                RateLimitError,
            )
        ),
        reraise=True,
    )
    async def fetch_meta(
        self,
        symbol: str,
    ) -> dict[str, str]:

        url = f"{self.base_url}/{symbol}"

        return await self._get(
            url=url,
            symbol=symbol,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception_type(
            (
                asyncio.TimeoutError,
                aiohttp.ClientError,
                RateLimitError,
            )
        ),
        reraise=True,
    )
    async def fetch_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> list[RawStockPrice]:

        url = f"{self.base_url}/{symbol}/prices"

        params = {
            "startDate": start_date,
            "endDate": end_date,
        }

        return await self._get(
            url=url,
            params=params,
            symbol=symbol,
        )

    async def _get(
        self,
        url: str,
        symbol: str,
        params: dict[str, str] | None = None,
    ) -> Any:

        async with (
            self.semaphore,
            self.session.get(
                url=url,
                headers=self.headers,
                params=params,
                timeout=self.timeout,
            ) as response,
        ):
            if response.status == 429:
                self.logger.warning(
                    "Tiingo rate limit hit for %s; retrying with backoff...",
                    symbol,
                )
                raise RateLimitError(f"Tiingo rate limit exceeded for {symbol}")

            if response.status in (401, 403):
                self.logger.error(
                    "Unauthorized Tiingo API call (HTTP %s).",
                    response.status,
                )
                raise UnauthorizationCallError(
                    f"HTTP {response.status}: Invalid or missing API token."
                )

            response.raise_for_status()

            return await response.json()
