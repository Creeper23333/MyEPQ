from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.models.garch import (
    fit_garch_grid,
    garch_realised_vol_forecast,
    garch_realised_vol_rms_forecast,
)
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

    def test_garch_likelihood_scores_return_before_variance_update(self) -> None:
        returns = np.array([0.001, 0.001, 0.080, 0.001, -0.075, 0.001] * 20)
        fitted = fit_garch_grid(returns)
        self.assertEqual(fitted["training_observations"], len(returns))

        variance = float(np.var(returns, ddof=1))
        expected_loss = 0.0
        for value in returns:
            expected_loss += 0.5 * (
                np.log(2.0 * np.pi) + np.log(variance) + (value**2) / variance
            )
            variance = max(
                fitted["omega"]
                + fitted["alpha"] * (value**2)
                + fitted["beta"] * variance,
                1e-12,
            )

        self.assertAlmostEqual(fitted["negative_log_likelihood"], expected_loss, places=9)

    def test_garch_rolling_variance_conversion_accounts_for_random_mean(self) -> None:
        frame = pd.DataFrame({"log_return": [0.1, 0.2]})
        params = {
            "omega": 0.09,
            "alpha": 0.0,
            "beta": 0.0,
            "training_return_variance": 0.09,
        }
        forecast = garch_realised_vol_rms_forecast(frame, params, window=3)

        # E[s^2] = (sum(x_i^2) + E[X^2] - E[(sum(x_i)+X)^2]/3) / 2
        expected_variance = (0.1**2 + 0.2**2 + 0.09 - ((0.1 + 0.2) ** 2 + 0.09) / 3) / 2
        self.assertAlmostEqual(forecast.iloc[1], np.sqrt(expected_variance), places=12)

    def test_garch_expected_standard_deviation_uses_gauss_hermite_target(self) -> None:
        frame = pd.DataFrame({"log_return": [0.1, 0.2]})
        params = {
            "omega": 0.09,
            "alpha": 0.0,
            "beta": 0.0,
            "training_return_variance": 0.09,
        }
        expected_std = garch_realised_vol_forecast(frame, params, window=3).iloc[1]
        rms_std = garch_realised_vol_rms_forecast(frame, params, window=3).iloc[1]

        rng = np.random.default_rng(17)
        next_returns = rng.normal(loc=0.0, scale=0.3, size=300_000)
        samples = np.column_stack(
            [
                np.full(len(next_returns), 0.1),
                np.full(len(next_returns), 0.2),
                next_returns,
            ]
        )
        monte_carlo_expected_std = float(np.std(samples, axis=1, ddof=1).mean())

        self.assertLessEqual(expected_std, rms_std)
        self.assertAlmostEqual(expected_std, monte_carlo_expected_std, delta=2e-4)

    def test_garch_forecast_does_not_use_future_returns(self) -> None:
        frame = pd.DataFrame(
            {"log_return": [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.03]}
        )
        params = {
            "omega": 0.001,
            "alpha": 0.2,
            "beta": 0.7,
            "training_return_variance": 0.01,
        }
        baseline = garch_realised_vol_forecast(frame, params, window=3)
        changed = frame.copy()
        changed.loc[5, "log_return"] = 0.8
        revised = garch_realised_vol_forecast(changed, params, window=3)

        self.assertTrue(
            np.allclose(
                baseline.iloc[:5].to_numpy(dtype=float),
                revised.iloc[:5].to_numpy(dtype=float),
                equal_nan=True,
            )
        )
        self.assertNotAlmostEqual(baseline.iloc[5], revised.iloc[5])


if __name__ == "__main__":
    unittest.main()
