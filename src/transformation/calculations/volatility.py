import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.utils.interface import FeatureCalculator

@dataclass
class VolatilityCalculator(FeatureCalculator):
    window: int = 20
    trading_days_per_year: int = 252

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if "log_return" not in df.columns:
            raise ValueError("VolatilityCalculator requires 'log_return'; run ReturnsCalculator first.")
        col = f"volatility_{self.window}d"
        df[col] = df["log_return"].rolling(window=self.window, min_periods=self.window).std()
        df[f"{col}_annualized"] = df[col] * np.sqrt(self.trading_days_per_year)
        return df