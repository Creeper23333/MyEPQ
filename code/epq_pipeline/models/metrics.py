"""Metric helpers and ranking utilities."""

from __future__ import annotations

import math

import numpy as np

from epq_pipeline.common.types import PerformanceRow


QLIKE_EPSILON = 1e-12


def qlike_loss(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    epsilon: float = QLIKE_EPSILON,
) -> float:
    """Return mean QLIKE after converting standard deviations to variances.

    The project predicts a rolling standard-deviation proxy. QLIKE is defined
    on positive variance quantities, so observed and forecast standard
    deviations are squared and floored only for numerical safety.
    """
    if epsilon <= 0.0:
        raise ValueError("QLIKE epsilon must be positive")
    actual = np.asarray(y_true, dtype=float)
    forecast = np.asarray(y_pred, dtype=float)
    if actual.shape != forecast.shape or actual.size == 0:
        raise ValueError("QLIKE needs non-empty arrays with matching shapes")
    if not np.all(np.isfinite(actual)) or not np.all(np.isfinite(forecast)):
        raise ValueError("QLIKE inputs must be finite")
    actual_variance = np.maximum(actual**2, epsilon)
    forecast_variance = np.maximum(forecast**2, epsilon)
    ratio = actual_variance / forecast_variance
    return float(np.mean(ratio - np.log(ratio) - 1.0))


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    error = y_true - y_pred
    mae = float(np.mean(np.abs(error)))
    mse = float(np.mean(error**2))
    rmse = float(math.sqrt(mse))
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "QLIKE": qlike_loss(y_true, y_pred),
    }


def performance_row(model: str, category: str, y_true: np.ndarray, y_pred: np.ndarray) -> PerformanceRow:
    scores = regression_metrics(y_true, y_pred)
    return PerformanceRow(
        model=model,
        category=category,
        mae=scores["MAE"],
        mse=scores["MSE"],
        rmse=scores["RMSE"],
        qlike=scores["QLIKE"],
    )


def rank_performance_rows(rows: list[PerformanceRow]) -> list[PerformanceRow]:
    return sorted(rows, key=lambda row: row.rmse)
