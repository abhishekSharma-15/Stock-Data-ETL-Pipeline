import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Base Directory of the project (3 levels up from this file).
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Directory from storing Raw Data.
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Start Date
START_DATE = datetime(2015, 1, 1)

# Yahoo Finance API URL
BASE_URL='https://query1.finance.yahoo.com/v8/finance/chart'

# Directory for storing Processed / Structured Data.
DATA_DIR = BASE_DIR / "data" 

# API Configuration
API_TIMEOUT = "10" # Seconds

# Logging
LOG_LEVEL = "INFO" # Logging level: (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Pipeline Configuration
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

# Yahoo API Parameters
YAHOO_RANGE = '1Y'
YAHOO_INTERVAL = '1d'

ROLLING_WINDOWS = {
    'volatility': 20,
    'ma_20d': 20,
    'ma_50d': 50
}

# Load environment variable
load_dotenv(BASE_DIR / '.env')
db_user = os.getenv('POSTGRES_USER', 'postgres')
db_pass = os.getenv('SQL_PASSWORD') or os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DB_HOST', 'postgres')
db_name = os.getenv('POSTGRES_DB', 'stock_pipeline')
db_port = os.getenv('DB_PORT', '5432')

DATABASE_URL = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'