"""GARCH utilities."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def fit_garch_grid(returns: np.ndarray) -> dict[str, float]:
    returns = np.asarray(returns, dtype=float)
    returns = returns[np.isfinite(returns)]
    sample_var = float(np.var(returns, ddof=1))
    if sample_var <= 0:
        raise ValueError("Training returns have zero variance")

    def neg_loglik(alpha: float, beta: float) -> float:
        if alpha < 0 or beta < 0 or alpha + beta >= 0.995:
            return float("inf")
        omega = max((1.0 - alpha - beta) * sample_var, 1e-12)
        var = sample_var
        total = 0.0
        for r in returns:
            var = max(omega + alpha * (r**2) + beta * var, 1e-12)
            total += 0.5 * (math.log(2.0 * math.pi) + math.log(var) + (r**2) / var)
        return total

    candidates: list[tuple[float, float]] = []
    for alpha in np.linspace(0.02, 0.22, 21):
        for beta in np.linspace(0.60, 0.97, 38):
            if alpha + beta < 0.995:
                candidates.append((float(alpha), float(beta)))

    coarse_alpha, coarse_beta = min(candidates, key=lambda pair: neg_loglik(*pair))

    fine_candidates: list[tuple[float, float]] = []
    for alpha in np.linspace(max(0.005, coarse_alpha - 0.04), min(0.35, coarse_alpha + 0.04), 33):
        for beta in np.linspace(max(0.10, coarse_beta - 0.05), min(0.989, coarse_beta + 0.05), 41):
            if alpha + beta < 0.995:
                fine_candidates.append((float(alpha), float(beta)))

    alpha, beta = min(fine_candidates, key=lambda pair: neg_loglik(*pair))
    omega = max((1.0 - alpha - beta) * sample_var, 1e-12)
    return {
        "omega": omega,
        "alpha": alpha,
        "beta": beta,
        "alpha_plus_beta": alpha + beta,
        "training_return_variance": sample_var,
        "negative_log_likelihood": neg_loglik(alpha, beta),
    }


def garch_next_variance(df: pd.DataFrame, params: dict[str, float]) -> pd.Series:
    returns = df["log_return"].to_numpy(dtype=float)
    omega = params["omega"]
    alpha = params["alpha"]
    beta = params["beta"]
    var = params["training_return_variance"]
    predictions: list[float | None] = []
    for r in returns:
        if not np.isfinite(r):
            predictions.append(None)
            continue
        next_var = max(omega + alpha * (r**2) + beta * var, 1e-12)
        predictions.append(next_var)
        var = next_var
    return pd.Series(predictions, index=df.index)


def garch_realised_vol_forecast(df: pd.DataFrame, params: dict[str, float], window: int = 30) -> pd.Series:
    returns = df["log_return"].to_numpy(dtype=float)
    next_variance = garch_next_variance(df, params).to_numpy(dtype=float)
    forecasts: list[float | None] = []
    known_count = window - 1
    for index, variance in enumerate(next_variance):
        start = index - known_count + 1
        if start < 0 or not np.isfinite(variance):
            forecasts.append(None)
            continue
        known_returns = returns[start : index + 1]
        if len(known_returns) != known_count or not np.all(np.isfinite(known_returns)):
            forecasts.append(None)
            continue
        expected_next_return = 0.0
        mean = float((known_returns.sum() + expected_next_return) / window)
        expected_sum_squares = float(np.sum((known_returns - mean) ** 2))
        expected_sum_squares += variance + (expected_next_return - mean) ** 2
        forecasts.append(math.sqrt(max(expected_sum_squares / (window - 1), 0.0)))
    return pd.Series(forecasts, index=df.index)

