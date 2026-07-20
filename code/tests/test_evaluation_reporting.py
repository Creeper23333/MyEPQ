from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.common.types import PerformanceRow
from epq_pipeline.reporting.evaluation import (
    build_block_bootstrap_rows,
    build_computational_rows,
    build_multidimensional_rows,
    build_permutation_importance_rows,
    build_regime_performance_rows,
    build_robustness_rows,
    build_test_segment_rows,
)


class EvaluationReportingTests(unittest.TestCase):
    def test_regime_rows_create_ranked_terciles(self) -> None:
        predictions = pd.DataFrame(
            {
                "actual": np.linspace(0.01, 0.12, 12),
                "rolling_historical": np.linspace(0.02, 0.13, 12),
                "garch_1_1": np.linspace(0.01, 0.12, 12),
            }
        )
        rows = build_regime_performance_rows(predictions)
        self.assertEqual({row["volatility_regime"] for row in rows}, {"Low", "Medium", "High"})
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["rank_by_RMSE"] == 1 for row in rows if row["model"] == "GARCH(1,1)"))

    def test_permutation_importance_detects_informative_feature(self) -> None:
        class FirstColumnModel:
            def predict(self, values: np.ndarray) -> np.ndarray:
                return values[:, 0]

        x = np.column_stack([np.linspace(0.0, 1.0, 40), np.ones(40)])
        y = x[:, 0].copy()
        rows = build_permutation_importance_rows(
            FirstColumnModel(), x, y, ("signal", "constant"), random_seed=5, repeats=5
        )
        self.assertEqual(rows[0]["feature"], "signal")
        self.assertGreater(float(rows[0]["mean_RMSE_increase"]), 0.0)
    def test_test_segment_rows_rank_each_half(self) -> None:
        predictions = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=6),
                "actual": [1.0] * 6,
                "rolling_historical": [1.2] * 6,
                "garch_1_1": [1.0] * 6,
            }
        )
        rows = build_test_segment_rows(predictions)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["model"], "GARCH(1,1)")
        self.assertEqual(rows[2]["test_segment"], "Second half")

    def test_block_bootstrap_is_deterministic_and_preserves_direction(self) -> None:
        predictions = pd.DataFrame(
            {
                "actual": np.linspace(0.1, 0.8, 40),
                "rolling_historical": np.linspace(0.2, 0.9, 40),
                "garch_1_1": np.linspace(0.1, 0.8, 40),
            }
        )
        first = build_block_bootstrap_rows(predictions, random_seed=7, samples=50, block_length=5)
        second = build_block_bootstrap_rows(predictions, random_seed=7, samples=50, block_length=5)
        self.assertEqual(first, second)
        garch = next(row for row in first if row["model"] == "GARCH(1,1)")
        self.assertLess(float(garch["bootstrap_95pct_upper"]), 0.0)

    def setUp(self) -> None:
        self.rows = [
            PerformanceRow("Rolling historical volatility", "Benchmark", 0.1, 0.02, 0.14),
            PerformanceRow("LSTM", "Machine learning", 0.2, 0.04, 0.20),
        ]
        self.timings = {
            "Rolling historical volatility": {"fit_seconds": 0.0, "predict_seconds": 0.001},
            "LSTM": {"fit_seconds": 2.0, "predict_seconds": 0.02},
        }
        self.complexities = {
            "Rolling historical volatility": {"measure": "fitted parameters", "value": 0},
            "LSTM": {"measure": "trainable parameters", "value": 1234},
        }

    def test_multidimensional_rows_include_evidence_not_only_scores(self) -> None:
        rows = build_multidimensional_rows(self.rows, self.timings, self.complexities)
        self.assertEqual(rows[0]["interpretability_level"], "High")
        self.assertIn("Direct persistence rule", rows[0]["explanation_evidence"])
        self.assertEqual(rows[1]["interpretability_level"], "Low")
        self.assertIn("1234", rows[1]["complexity"])

    def test_computational_rows_add_fit_and_prediction_time(self) -> None:
        rows = build_computational_rows(self.timings, self.complexities, 100, 20)
        self.assertEqual(rows[1]["total_seconds"], "2.020000")
        self.assertEqual(rows[1]["train_rows"], 100)

    def test_robustness_rows_are_relative_to_rolling_benchmark(self) -> None:
        rows = build_robustness_rows(14, self.rows, "2025-01-01", "2025-10-01", "2025-10-02", "2026-01-01")
        self.assertEqual(rows[0]["RMSE_vs_rolling_percent"], "0.000")
        self.assertEqual(rows[1]["RMSE_vs_rolling_percent"], "42.857")


if __name__ == "__main__":
    unittest.main()
