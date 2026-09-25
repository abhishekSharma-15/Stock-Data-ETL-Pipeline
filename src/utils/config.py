import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

MAX_CONCURRENCY: int = 5

# Base Directory of the project (3 levels up from this file).
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

# Directory from storing Raw Data.
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Start Date
START_DATE = date(2026, 9, 20)

# Yahoo Finance API URL
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart"

# Alpha Vantage API URL
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query?"
FUNCTION = "TIME_SERIES_DAILY"

# Tiingo API URL
TIINGO_URL = os.getenv("TIINGO_URL")
TIINGO_API_TOKEN = os.getenv("API_TIINGO")

# Directory for storing Processed / Structured Data.
DATA_DIR = BASE_DIR / "data"

# API Configuration
API_TIMEOUT = "10"  # Seconds

# Logging
LOG_LEVEL = "INFO"  # Logging level: (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Pipeline Configuration
STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]

# Yahoo API Parameters
YAHOO_RANGE = "1Y"
YAHOO_INTERVAL = "1d"

ROLLING_WINDOWS = {"volatility": 20, "ma_20d": 20, "ma_50d": 50}

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

# Minio Environment Variable
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "stock-data-raw")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

# Load environment variable
db_user = os.getenv("POSTGRES_USER", "postgres")
db_pass = os.getenv("SQL_PASSWORD") or os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_HOST", "postgres")
db_name = os.getenv("POSTGRES_DB", "stock_pipeline")
db_port = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
