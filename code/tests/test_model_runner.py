from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.pipeline.model_runner import align_forecasts_by_date


class ModelRunnerTests(unittest.TestCase):
    def test_forecasts_are_aligned_by_date_not_dataframe_index(self) -> None:
        source_dates = pd.Series(pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03"]))
        forecasts = pd.Series([0.1, 0.2, 0.3], index=[50, 51, 52])
        target_dates = pd.Series(pd.to_datetime(["2026-01-03", "2026-01-01"]))
        aligned = align_forecasts_by_date(source_dates, forecasts, target_dates)
        self.assertTrue(np.allclose(aligned, [0.3, 0.1]))

    def test_missing_forecast_date_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            align_forecasts_by_date(
                pd.Series(pd.to_datetime(["2026-01-01"])),
                pd.Series([0.1]),
                pd.Series(pd.to_datetime(["2026-01-02"])),
            )


if __name__ == "__main__":
    unittest.main()
