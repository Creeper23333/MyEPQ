"""Metric helpers and ranking utilities."""

from __future__ import annotations

import math

import numpy as np

from epq_pipeline.common.types import PerformanceRow


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    error = y_true - y_pred
    mae = float(np.mean(np.abs(error)))
    mse = float(np.mean(error**2))
    rmse = float(math.sqrt(mse))
    return {"MAE": mae, "MSE": mse, "RMSE": rmse}


def performance_row(model: str, category: str, y_true: np.ndarray, y_pred: np.ndarray) -> PerformanceRow:
    scores = regression_metrics(y_true, y_pred)
    return PerformanceRow(
        model=model,
        category=category,
        mae=scores["MAE"],
        mse=scores["MSE"],
        rmse=scores["RMSE"],
    )


def rank_performance_rows(rows: list[PerformanceRow]) -> list[PerformanceRow]:
    return sorted(rows, key=lambda row: row.rmse)

