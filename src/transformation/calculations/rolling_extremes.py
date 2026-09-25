from dataclasses import dataclass

import pandas as pd

from src.utils.interface import FeatureCalculator


@dataclass
class RollingExtremesCalculator(FeatureCalculator):
    window: int = 20

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df[f"rolling_high_{self.window}d"] = (
            df["high"].rolling(self.window, min_periods=self.window).max()
        )
        df[f"rolling_low_{self.window}d"] = (
            df["low"].rolling(self.window, min_periods=self.window).min()
        )
        return df
