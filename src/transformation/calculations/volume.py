from dataclasses import dataclass

import pandas as pd

from src.utils.interface import FeatureCalculator


@dataclass
class VolumeFeaturesCalculator(FeatureCalculator):
    windows: tuple[int, ...] = (20, 50)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for window in self.windows:
            ma_col = f"volume_ma_{window}d"
            ratio_col = f"volume_ratio_{window}d"

            df[ma_col] = df["volume"].rolling(window=window, min_periods=window).mean()
            df[ratio_col] = df["volume"] / df[ma_col]
        return df
