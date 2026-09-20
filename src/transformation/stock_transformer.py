"""
Stock Price Transformation Logic

Responsibilities:
- Clean raw OHLCV data
- Compute returns- and volatility- based features
"""

import pandas as pd
import numpy as np
from src.utils.logger import get_logger
from src.utils.config import ROLLING_WINDOWS

class StockTransformer:
    """
    Cleans the raw equity price data (csv format) and applies transformation and features
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standarize raw equity price data. 
        
        Parameters:
        -----------
        df: pd.DataFrame
            Parsed stock price data sorted by date.

        Returns:
        --------
        pd.DataFrame
            Cleaned data ready for feature engineering.
        """

        self.logger.info(f'Cleaning data')

        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Enforce numeric consistency for downstream calculations
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].astype(float)

        df = df.drop_duplicates(subset=['date'])
        df = df.dropna(subset=['close'])

        return df
    
    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds returns-based and trend-based features to cleaned data.

        Parameters:
        -----------
        df: pd.DataFrame
            Cleaned stock price data sorted by data.

        Returns:
        --------
        pd.DataFrame
            DataFrame with feature engineering data.
        """
        
        self.logger.info(f'Adding features')

        df = df.copy()
        df['daily_return'] = df['close'].pct_change()

        df['log_return'] = np.log(df['close']/df['close'].shift(1))
        df['volatility_20d'] = (df['log_return'].rolling(ROLLING_WINDOWS['volatility']).std())
        
        df['ma_20d'] = df['close'].rolling(ROLLING_WINDOWS['ma_20d']).mean()
        df['ma_50d'] = df['close'].rolling(ROLLING_WINDOWS['ma_50d']).mean()

        return df
    
