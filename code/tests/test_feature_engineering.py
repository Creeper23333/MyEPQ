from __future__ import annotations

import sys
import tempfile
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
    chronological_split_by_date,
    ensure_realised_volatility,
    fit_standardization_stats,
    load_dataset,
)
from epq_pipeline.config import LSTMConfig, ModelRunConfig
from epq_pipeline.models.lstm import validation_count_for_sequence_count


class FeatureEngineeringTests(unittest.TestCase):
    def test_active_target_volatility_duplicate_is_removed_from_model_features(self) -> None:
        config_30 = ModelRunConfig(rv_window=30)
        self.assertNotIn("rolling_return_std_30d", config_30.feature_cols)
        self.assertNotIn("rolling_return_std_30d", config_30.lstm_feature_cols)
        self.assertIn("rolling_return_std_14d", config_30.feature_cols)

        config_14 = ModelRunConfig(rv_window=14)
        self.assertNotIn("rolling_return_std_14d", config_14.feature_cols)
        self.assertNotIn("rolling_return_std_14d", config_14.lstm_feature_cols)
        self.assertIn("rolling_return_std_30d", config_14.feature_cols)
        self.assertIn("rolling_return_std_30d", config_14.lstm_feature_cols)

    def test_fixed_cutoff_does_not_move_old_test_rows_when_data_is_appended(self) -> None:
        original = pd.DataFrame(
            {
                "date": pd.date_range("2025-11-13", periods=6, freq="D"),
                "value": np.arange(6),
            }
        )
        initial = chronological_split_by_date(original, "2025-11-16")
        appended = pd.concat(
            [
                original,
                pd.DataFrame(
                    {
                        "date": pd.date_range("2025-11-19", periods=3, freq="D"),
                        "value": np.arange(6, 9),
                    }
                ),
            ],
            ignore_index=True,
        )
        refreshed = chronological_split_by_date(appended, "2025-11-16")
        self.assertEqual(initial.train["date"].tolist(), refreshed.train["date"].tolist())
        self.assertEqual(
            initial.test["date"].tolist(),
            refreshed.test["date"].iloc[: len(initial.test)].tolist(),
        )

    def test_different_target_windows_share_test_dates_after_fixed_cutoff(self) -> None:
        frame_14 = pd.DataFrame(
            {"date": pd.date_range("2025-11-01", "2025-11-20", freq="D")}
        )
        frame_30 = pd.DataFrame(
            {"date": pd.date_range("2025-11-05", "2025-11-20", freq="D")}
        )
        split_14 = chronological_split_by_date(frame_14, "2025-11-16")
        split_30 = chronological_split_by_date(frame_30, "2025-11-16")
        self.assertEqual(split_14.test["date"].tolist(), split_30.test["date"].tolist())

    def test_model_input_loader_rejects_daily_gaps_and_corrupt_returns(self) -> None:
        dates = pd.date_range("2026-01-01", periods=5, freq="D")
        close = pd.Series([100.0, 101.0, 99.0, 102.0, 103.0])
        returns = np.log(close / close.shift(1))
        valid = pd.DataFrame(
            {
                "date": dates,
                "close": close,
                "log_return": returns,
                "realised_volatility_2d": returns.rolling(2).std(ddof=1),
                "volume": [10.0] * 5,
                "trade_count": [2] * 5,
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "processed.csv"
            valid.to_csv(path, index=False)
            loaded = load_dataset(path, "realised_volatility_2d", 2)
            self.assertEqual(len(loaded), 5)

            gap = valid.copy()
            gap.loc[3, "date"] = pd.Timestamp("2026-01-05")
            gap.loc[4, "date"] = pd.Timestamp("2026-01-06")
            gap.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "continuous"):
                load_dataset(path, "realised_volatility_2d", 2)

            corrupt_return = valid.copy()
            corrupt_return.loc[2, "log_return"] = 0.5
            corrupt_return.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "log returns"):
                load_dataset(path, "realised_volatility_2d", 2)

    def test_lstm_validation_count_matches_chronological_training_split(self) -> None:
        config = LSTMConfig(validation_fraction=0.15)
        self.assertEqual(validation_count_for_sequence_count(921, config), 138)

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
        self.assertIn("target_date", frame.columns)
        self.assertTrue((frame["target_date"] > frame["date"]).all())
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
