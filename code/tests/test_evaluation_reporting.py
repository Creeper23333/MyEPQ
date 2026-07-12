from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.common.types import PerformanceRow
from epq_pipeline.reporting.evaluation import (
    build_computational_rows,
    build_multidimensional_rows,
    build_robustness_rows,
)


class EvaluationReportingTests(unittest.TestCase):
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
