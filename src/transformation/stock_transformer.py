from logging import Logger

import numpy as np
import pandas as pd

from src.transformation.calculations.intraday import IntradayFeaturesCalculator
from src.transformation.calculations.moving_average import MovingAverageCalculator
from src.transformation.calculations.returns import ReturnsCalculator
from src.transformation.calculations.rolling_extremes import RollingExtremesCalculator
from src.transformation.calculations.volatility import VolatilityCalculator
from src.transformation.calculations.volume import VolumeFeaturesCalculator
from src.utils.interface import FeatureCalculator, Transformer
from src.utils.models import StockPriceData


class StockTransformer(Transformer):
    def __init__(
        self, logger: Logger, calculations: list[FeatureCalculator] | None = None
    ) -> None:

        self.logger = logger
        self.calculations = calculations or [
            ReturnsCalculator(),
            IntradayFeaturesCalculator(),
            MovingAverageCalculator(),
            VolatilityCalculator(),
            RollingExtremesCalculator(),
            VolumeFeaturesCalculator(),
        ]

    def transform(self, data: list[StockPriceData]) -> pd.DataFrame:

        if not data:
            self.logger.warning("No data provided to Transformer")
            return pd.DataFrame()

        df = self._to_dataframe(data)
        df = self._clean_and_order(df)

        for calculator in self.calculations:
            df = calculator.calculate(df)

        return self._clean_invalid_values(df)

    def _to_dataframe(self, data: list[StockPriceData]) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "date": p.date,
                    "open": p.open,
                    "high": p.high,
                    "low": p.low,
                    "close": p.close,
                    "volume": p.volume,
                }
                for p in data
            ]
        )

    def _clean_and_order(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], utc=True)

        return (
            df.sort_values("date")
            .drop_duplicates(subset="date", keep="last")
            .reset_index(drop=True)
        )

    def _clean_invalid_values(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.replace([np.inf, -np.inf], np.nan)
