import asyncio
from src.utils.logger import get_logger
from src.utils.config import STOCK_SYMBOLS
from src.orchestration.orchestrator import StockOrchestrator
from src.storage.stock_repository import StockRepository
from src.storage.engine import create_database_engine
from src.storage.init.init_db import init_db

async def main():
    logger = get_logger('Stock Price Pipeline')

    engine = create_database_engine()_ 
    init_db(engine)

    repository = StockRepository(engine)    
    orchestrator = StockOrchestrator(
        logger,
        repository,
        STOCK_SYMBOLS
    )
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(main())