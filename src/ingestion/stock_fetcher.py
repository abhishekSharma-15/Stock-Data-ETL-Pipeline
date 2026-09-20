from typing import Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from datetime import datetime
from src.utils.execeptions import YahooRateLimitError
import asyncio
import aiohttp
from src.utils.config import (
    API_TIMEOUT,
    BASE_URL,
    YAHOO_INTERVAL
)

semaphore = asyncio.Semaphore(3)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=2,
        max=10
    ),
    retry=retry_if_exception_type(
        (
            asyncio.TimeoutError,
            aiohttp.ClientError,
            YahooRateLimitError
        )
    ),
    reraise=True
)
async def fetch(
    symbol: str,
    session: aiohttp.ClientSession,
    start_date: datetime = datetime(2015, 1, 1),
    end_date: datetime = datetime.today(),
) -> dict[str, Any]:
    
    url = f'{BASE_URL}/{symbol}'
    params={
        "period1": int(start_date.timestamp()),
        "period2": int(end_date.timestamp()),
        "interval": YAHOO_INTERVAL,
    }

    async with semaphore:
        async with session.get(
            url=url,
            params=params,
            timeout=aiohttp.ClientTimeout(
                total=float(API_TIMEOUT)
            )
        ) as response:

            if response.status == 429:
                raise YahooRateLimitError(
                    f"Yahoo Finance rate limit exceeded for {symbol}"
                )

            response.raise_for_status()
            print(response)
            return await response.json()

    # async with session.get(
    #     url,
    #     params=params,
    #     timeout=aiohttp.ClientTimeout(total=float(API_TIMEOUT))
    # ) as response:

    #     if response.status == 429:
    #         raise YahooRateLimitError(
    #             f"Yahoo Finance rate limit exceeded for {symbol}"
    #         )

    #     response.raise_for_status()
    #     return await response.json()