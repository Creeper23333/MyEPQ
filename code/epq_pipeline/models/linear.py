"""Lagged linear regression model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LinearRegressionArtifacts:
    coefficients: np.ndarray
    feature_names: tuple[str, ...]


def fit_linear_regression(x: np.ndarray, y: np.ndarray, feature_names: tuple[str, ...]) -> LinearRegressionArtifacts:
    x_design = np.column_stack([np.ones(len(x)), x])
    ridge = np.eye(x_design.shape[1]) * 1e-8
    ridge[0, 0] = 0.0
    coefficients = np.linalg.solve(x_design.T @ x_design + ridge, x_design.T @ y)
    return LinearRegressionArtifacts(coefficients=coefficients, feature_names=feature_names)


def predict_linear_regression(x: np.ndarray, artifacts: LinearRegressionArtifacts) -> np.ndarray:
    x_design = np.column_stack([np.ones(len(x)), x])
    return np.clip(x_design @ artifacts.coefficients, 0.0, None)


def coefficient_rows(artifacts: LinearRegressionArtifacts) -> list[dict[str, str]]:
    rows = [{"term": "intercept", "coefficient": f"{artifacts.coefficients[0]:.10f}"}]
    for feature_name, coefficient in zip(artifacts.feature_names, artifacts.coefficients[1:]):
        rows.append({"term": feature_name, "coefficient": f"{coefficient:.10f}"})
    return rows

