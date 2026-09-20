"""
Stock Data Parser Logic.

Responsibilities:
- Parse OHLCV stock price data from raw API responses.
"""

import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger

class StockDataParser:
    """
    Converts raw stock price data from JSON format into Pandas DataFrame.
    """

    def __init__(self):
        # self.symbol = symbol
        self.logger = get_logger(self.__class__.__name__)

    def parse(self, raw_data:dict) -> pd.DataFrame:
        """
        Parse raw equity price data into OHLCV format.

        Parameters:
        -----------
        raw_data: dict
            Raw API response containing stock price data.

        Returns:
        --------
        pd.DataFrame
            Parsed OHLCV stock price data.
        """

        try:
            result = raw_data['chart']['result'][0]
            timestamps = result['timestamp']
            quote = result['indicators']['quote'][0]

            df = pd.DataFrame({
                'date': [datetime.fromtimestamp(ts).date() for ts in timestamps],
                'open': quote['open'],
                'high': quote['high'],
                'low': quote['low'],
                'close': quote['close'],
                'volume': quote['volume']
            })

            df = df.dropna(subset=['close'])
            df = df[df['volume']>0]
            
            self.logger.info(f'Parsed {len(df)} rows of {self.symbol}')
            return df
        
        except Exception as e:
            self.logger.error(f'Failed to parsed data: {e}')
            raise