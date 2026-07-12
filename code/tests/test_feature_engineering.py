from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.features.engineering import (
    add_base_features,
    apply_standardization,
    build_lstm_sequences,
    build_modelling_frame,
    chronological_split,
    ensure_realised_volatility,
    fit_standardization_stats,
)


class FeatureEngineeringTests(unittest.TestCase):
    def test_realised_volatility_can_be_derived_for_robustness_window(self) -> None:
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=5, freq="D"),
                "log_return": [np.nan, 0.01, -0.02, 0.03, -0.01],
            }
        )
        result = ensure_realised_volatility(df, "realised_volatility_3d", 3)
        expected = pd.Series(df["log_return"]).rolling(3).std(ddof=1)
        self.assertTrue(np.allclose(result["realised_volatility_3d"], expected, equal_nan=True))

    def test_realised_volatility_window_must_have_two_rows(self) -> None:
        with self.assertRaises(ValueError):
            ensure_realised_volatility(pd.DataFrame({"log_return": [0.1]}), "rv", 1)

    def test_standardization_handles_zero_std_columns(self) -> None:
        values = np.array([[1.0, 2.0], [1.0, 4.0], [1.0, 6.0]])
        stats = fit_standardization_stats(values)
        transformed = apply_standardization(values, stats)
        self.assertTrue(np.allclose(transformed[:, 0], 0.0))
        self.assertAlmostEqual(float(transformed[:, 1].mean()), 0.0, places=7)

    def test_lstm_sequence_split_matches_train_boundary(self) -> None:
        features = np.arange(40, dtype=float).reshape(10, 4)
        targets = np.arange(10, dtype=float)
        dates = pd.date_range("2026-01-01", periods=10, freq="D").to_numpy()
        sequences = build_lstm_sequences(features, targets, dates, split_index=7, sequence_length=3)
        self.assertEqual(len(sequences["x_train"]), 5)
        self.assertEqual(len(sequences["x_test"]), 3)
        self.assertEqual(float(sequences["y_test"][0]), 7.0)

    def test_modelling_frame_drops_missing_rows(self) -> None:
        periods = 12
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=periods, freq="D"),
                "close": list(range(1, periods + 1)),
                "log_return": [np.nan] + [0.1 + 0.01 * index for index in range(periods - 1)],
                "realised_volatility_30d": [np.nan, np.nan] + [0.5 + 0.02 * index for index in range(periods - 2)],
                "volume": [1] * periods,
                "trade_count": [1] * periods,
            }
        )
        featured = add_base_features(df, "realised_volatility_30d", "target")
        frame = build_modelling_frame(
            featured,
            (
                "realised_volatility_30d",
                "log_return",
                "abs_return",
                "log_volume",
                "log_trade_count",
                "return_lag_1",
                "abs_return_lag_1",
                "rv_lag_1",
                "rolling_abs_return_7d",
                "rolling_return_std_7d",
            ),
            "target",
        )
        split = chronological_split(frame, 0.5)
        self.assertGreater(len(frame), 1)
        self.assertLessEqual(len(split.train), len(frame))
        self.assertLessEqual(len(split.test), len(frame))

    def test_chronological_split_requires_rows_on_both_sides(self) -> None:
        frame = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3, freq="D"),
                "value": [1.0, 2.0, 3.0],
            }
        )
        with self.assertRaises(ValueError):
            chronological_split(frame, 0.0)
        with self.assertRaises(ValueError):
            chronological_split(frame, 1.0)


if __name__ == "__main__":
    unittest.main()
