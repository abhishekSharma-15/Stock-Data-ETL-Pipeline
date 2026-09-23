import pandas as pd
import numpy as np
from src.utils.interface import FeatureCalculator

class ReturnsCalculator(FeatureCalculator):
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["daily_return"] = df["close"].pct_change()
        df["log_return"] = np.log(df["close"] / df["close"].shift(1))
        return df