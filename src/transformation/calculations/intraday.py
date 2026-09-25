import pandas as pd

from src.utils.interface import FeatureCalculator


class IntradayFeaturesCalculator(FeatureCalculator):
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["intraday_range"] = (df["high"] - df["low"]) / df["open"]
        df["intraday_return"] = (df["close"] - df["open"]) / df["open"]
        return df
