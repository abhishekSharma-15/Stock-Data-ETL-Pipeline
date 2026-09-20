from dataclasses import dataclass
# from src.ingestion.stock_fetcher import StockFetcher
from src.ingestion.stock_parser import StockDataParser
from src.transformation.stock_transformer import StockTransformer
# from storage.stock_repository import PostgresLoader

@dataclass
class ETLDependencies:
    # fetcher: StockFetcher
    parser: StockDataParser
    transformer: StockTransformer
    # loader: PostgresLoader