from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.models.metrics import performance_row, rank_performance_rows, regression_metrics


class MetricTests(unittest.TestCase):
    def test_regression_metrics_are_zero_for_perfect_predictions(self) -> None:
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        metrics = regression_metrics(y_true, y_pred)
        self.assertEqual(metrics["MAE"], 0.0)
        self.assertEqual(metrics["MSE"], 0.0)
        self.assertEqual(metrics["RMSE"], 0.0)

    def test_rank_performance_rows_sorts_by_rmse(self) -> None:
        y_true = np.array([1.0, 2.0, 3.0])
        row_a = performance_row("A", "Category", y_true, np.array([1.0, 2.0, 3.0]))
        row_b = performance_row("B", "Category", y_true, np.array([0.0, 0.0, 0.0]))
        ranked = rank_performance_rows([row_b, row_a])
        self.assertEqual(ranked[0].model, "A")


if __name__ == "__main__":
    unittest.main()
