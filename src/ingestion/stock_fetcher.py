from typing import Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from datetime import datetime
from utils.exceptions import RateLimitError, UnauthorizationCallError
import asyncio
import aiohttp
from src.utils.config import (
    API_TIMEOUT,
    TIINGO_URL,
    TIINGO_API_TOKEN
)

semaphore = asyncio.Semaphore(1)

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
            aiohttp.ClientError
        )
    ),
    reraise=True
)
async def fetch(
    symbol: str,
    session: aiohttp.ClientSession,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> dict[str, Any]:

    start_date = start_date or datetime(2015, 1, 1)
    end_date = end_date or datetime.now()   
        
    url = f'{TIINGO_URL}/{symbol}/prices'
    params={
        'startDate': start_date.strftime("%Y-%m-%d"),
        'endDate': end_date.strftime("%Y-%m-%d"),
    }

    headers = {
        "Authorization": f"Token {TIINGO_API_TOKEN}"
    }

    async with semaphore:
        async with session.get(
            url=url,
            params=params,
            headers=headers,
            timeout=aiohttp.ClientTimeout(
                total=float(API_TIMEOUT)
            )
        ) as response:

            if response.status == 429:
                raise RateLimitError(
                    f"Tiingo rate limit exceeded for {symbol}"
                )

            if response.status == 403:
                raise UnauthorizationCallError()

            response.raise_for_status()
            return await response.json()