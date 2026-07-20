"""GARCH utilities."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


GAUSS_HERMITE_NODE_COUNT = 80
_GH_NODES, _GH_WEIGHTS = np.polynomial.hermite.hermgauss(GAUSS_HERMITE_NODE_COUNT)


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
            # Score r_t using information available through t-1. Only after
            # observing r_t may its squared shock update the next variance.
            total += 0.5 * (math.log(2.0 * math.pi) + math.log(var) + (r**2) / var)
            var = max(omega + alpha * (r**2) + beta * var, 1e-12)
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
        "training_observations": int(len(returns)),
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


def garch_realised_vol_rms_forecast(
    df: pd.DataFrame,
    params: dict[str, float],
    window: int = 30,
) -> pd.Series:
    """Return sqrt(E[s^2]), retained as a target-conversion sensitivity."""
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
        # For one random next return X and n-1 known returns, the expected
        # sample sum of squares is E[sum(z_i^2) - n * mean(z)^2].  The
        # variance of X therefore enters both E[X^2] and E[mean(z)^2]; simply
        # inserting E[X] into the sample-variance formula would over-count the
        # conditional variance by variance / n.
        expected_next_return = 0.0
        known_sum = float(known_returns.sum())
        known_sum_squares = float(np.sum(known_returns**2))
        expected_next_square = variance + expected_next_return**2
        expected_total_sum_square = known_sum_squares + expected_next_square
        expected_squared_total = (
            (known_sum + expected_next_return) ** 2 + variance
        )
        expected_sum_squares = expected_total_sum_square - expected_squared_total / window
        forecasts.append(math.sqrt(max(expected_sum_squares / (window - 1), 0.0)))
    return pd.Series(forecasts, index=df.index)


def garch_realised_vol_forecast(
    df: pd.DataFrame,
    params: dict[str, float],
    window: int = 30,
) -> pd.Series:
    """Return E[s] for the next rolling sample standard deviation.

    The evaluation target is a standard deviation rather than a variance. For
    squared-error evaluation the relevant conditional point forecast is E[s],
    not sqrt(E[s^2]). Under the same zero-mean Gaussian assumption used by the
    GARCH likelihood, 80-point Gauss-Hermite quadrature integrates over the one
    unknown next return while all preceding returns in the window are observed.
    """
    if window < 2:
        raise ValueError("Realised-volatility window must contain at least two returns")
    returns = df["log_return"].to_numpy(dtype=float)
    next_variance = garch_next_variance(df, params).to_numpy(dtype=float)
    forecasts: list[float | None] = []
    known_count = window - 1
    normal_weights = _GH_WEIGHTS / math.sqrt(math.pi)

    for index, variance in enumerate(next_variance):
        start = index - known_count + 1
        if start < 0 or not np.isfinite(variance):
            forecasts.append(None)
            continue
        known_returns = returns[start : index + 1]
        if len(known_returns) != known_count or not np.all(np.isfinite(known_returns)):
            forecasts.append(None)
            continue

        # hermgauss integrates exp(-x^2); sqrt(2)*x therefore supplies nodes
        # for a standard normal variable and weights must be divided by sqrt(pi).
        next_returns = math.sqrt(2.0 * max(float(variance), 0.0)) * _GH_NODES
        known_sum = float(known_returns.sum())
        known_sum_squares = float(np.sum(known_returns**2))
        total_sums = known_sum + next_returns
        total_sum_squares = known_sum_squares + next_returns**2
        sample_variances = (
            total_sum_squares - (total_sums**2) / window
        ) / (window - 1)
        sample_standard_deviations = np.sqrt(np.maximum(sample_variances, 0.0))
        forecasts.append(float(np.dot(normal_weights, sample_standard_deviations)))

    return pd.Series(forecasts, index=df.index)
