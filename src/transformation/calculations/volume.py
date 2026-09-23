import pandas as pd
from dataclasses import dataclass
from src.utils.interface import FeatureCalculator

@dataclass
class VolumeFeaturesCalculator(FeatureCalculator):
    window: int = 20

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        ma_col = f"volume_ma_{self.window}d"
        df[ma_col] = df["volume"].rolling(self.window, min_periods=self.window).mean()
        df[f"volume_ratio_{self.window}d"] = df["volume"] / df[ma_col]
        return df