from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


class SQLExecutor:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def fetch_one(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> Any | None:
        async with self.engine.connect() as conn:
            result = await conn.execute(
                text(query),
                params or {},
            )
            return result.fetchone()

    async def execute(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(
                text(query),
                params or {},
            )

    async def execute_returning_one(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> Any | None:

        async with self.engine.begin() as conn:
            result = await conn.execute(
                text(query),
                params or {},
            )

            return result.scalar()
