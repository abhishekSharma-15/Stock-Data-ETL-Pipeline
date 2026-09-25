from dataclasses import dataclass

import pandas as pd

from src.utils.interface import FeatureCalculator


@dataclass
class MovingAverageCalculator(FeatureCalculator):
    windows: tuple[int, ...] = (20, 50)
    column: str = "close"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for w in self.windows:
            df[f"ma_{w}d"] = df[self.column].rolling(window=w, min_periods=w).mean()
        return df
