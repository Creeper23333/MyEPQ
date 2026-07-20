"""Structured evidence for comparison beyond forecast-error metrics."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from epq_pipeline.common.types import PerformanceRow


MODEL_ASSESSMENTS: dict[str, dict[str, str]] = {
    "Rolling historical volatility": {
        "interpretability": "High",
        "explanation_evidence": "Direct persistence rule: tomorrow's forecast equals today's realised volatility.",
        "interpretability_limit": "Cannot explain changes beyond persistence in the rolling target.",
        "reproducibility": "High: no fitting, tuning, or external ML framework required.",
        "risk_use": "Transparent reference forecast suitable for communicating a current volatility regime.",
    },
    "GARCH(1,1)": {
        "interpretability": "High",
        "explanation_evidence": "Omega, alpha, and beta represent baseline variance, shock response, and persistence; 80-point Gauss-Hermite quadrature maps conditional variance to E[s].",
        "interpretability_limit": "Conversion from one-day conditional variance to a rolling standard-deviation target remains an additional modelled step.",
        "reproducibility": "High: deterministic grid search with recorded parameter estimates.",
        "risk_use": "Combines interpretable volatility dynamics with the strongest tested accuracy, although the rolling-target conversion remains a methodological caveat.",
    },
    "Lagged linear regression": {
        "interpretability": "High",
        "explanation_evidence": "Every standardised feature has an exported signed coefficient.",
        "interpretability_limit": "Correlated lag and rolling features make individual coefficients harder to interpret causally.",
        "reproducibility": "High: deterministic closed-form fit with fixed feature construction.",
        "risk_use": "Offers a transparent forecast when users need both low error and an auditable feature relationship.",
    },
    "Random Forest": {
        "interpretability": "Medium",
        "explanation_evidence": "Impurity-based and repeated holdout permutation importance identify the variables used across the forest; OOB diagnostics audit training-period generalisation.",
        "interpretability_limit": "Global importance is associational, not causal, and does not explain the direction or one individual prediction.",
        "reproducibility": "Medium-High: fixed seed and recorded hyperparameters, but bootstrap fitting is more complex.",
        "risk_use": "Can capture nonlinear relationships, but needs a clear accuracy gain before reduced transparency is justified.",
    },
    "LSTM": {
        "interpretability": "Low",
        "explanation_evidence": "Architecture, sequence inputs, training history, and parameter count are recorded.",
        "interpretability_limit": "Internal recurrent states and distributed weights do not provide a direct forecast explanation.",
        "reproducibility": "Medium: fixed seeds and early stopping are recorded, but results depend on PyTorch and optimisation.",
        "risk_use": "Potentially useful for sequence effects, but difficult to audit and currently not accurate enough to displace simple models.",
    },
}

MODEL_PREDICTION_COLUMNS = {
    "Rolling historical volatility": "rolling_historical",
    "GARCH(1,1)": "garch_1_1",
    "Lagged linear regression": "lagged_linear_regression",
    "Random Forest": "random_forest",
    "LSTM": "lstm",
}


def build_computational_rows(
    timings: dict[str, dict[str, float]],
    complexities: dict[str, dict[str, Any]],
    train_rows: int,
    test_rows: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model, timing in timings.items():
        complexity = complexities[model]
        rows.append(
            {
                "model": model,
                "fit_seconds": f"{timing['fit_seconds']:.6f}",
                "predict_seconds": f"{timing['predict_seconds']:.6f}",
                "total_seconds": f"{timing['fit_seconds'] + timing['predict_seconds']:.6f}",
                "complexity_measure": complexity["measure"],
                "complexity_value": complexity["value"],
                "train_rows": train_rows,
                "test_rows": test_rows,
                "timing_note": "Single local CPU run; timings compare project implementations and are not hardware-independent benchmarks.",
            }
        )
    return rows


def build_multidimensional_rows(
    ranked_rows: list[PerformanceRow],
    timings: dict[str, dict[str, float]],
    complexities: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rank, result in enumerate(ranked_rows, start=1):
        assessment = MODEL_ASSESSMENTS[result.model]
        timing = timings[result.model]
        complexity = complexities[result.model]
        rows.append(
            {
                "accuracy_rank_by_RMSE": rank,
                "model": result.model,
                "category": result.category,
                "MAE": f"{result.mae:.8f}",
                "RMSE": f"{result.rmse:.8f}",
                "interpretability_level": assessment["interpretability"],
                "explanation_evidence": assessment["explanation_evidence"],
                "main_interpretability_limit": assessment["interpretability_limit"],
                "fit_seconds": f"{timing['fit_seconds']:.6f}",
                "predict_seconds": f"{timing['predict_seconds']:.6f}",
                "complexity": f"{complexity['value']} {complexity['measure']}",
                "reproducibility_assessment": assessment["reproducibility"],
                "risk_management_assessment": assessment["risk_use"],
            }
        )
    return rows


def build_robustness_rows(
    window: int,
    ranked_rows: list[PerformanceRow],
    train_start: str,
    train_end: str,
    test_start: str,
    test_end: str,
) -> list[dict[str, Any]]:
    rolling_rmse = next(row.rmse for row in ranked_rows if row.model == "Rolling historical volatility")
    return [
        {
            "volatility_window_days": window,
            "rank_by_RMSE": rank,
            "model": result.model,
            "MAE": f"{result.mae:.8f}",
            "MSE": f"{result.mse:.8f}",
            "RMSE": f"{result.rmse:.8f}",
            "RMSE_vs_rolling_percent": f"{((result.rmse / rolling_rmse) - 1.0) * 100.0:.3f}",
            "train_period": f"{train_start} to {train_end}",
            "test_period": f"{test_start} to {test_end}",
        }
        for rank, result in enumerate(ranked_rows, start=1)
    ]


def build_test_segment_rows(predictions: pd.DataFrame) -> list[dict[str, Any]]:
    """Report whether the primary ranking survives early and late test halves."""
    midpoint = len(predictions) // 2
    segments = (
        ("First half", predictions.iloc[:midpoint]),
        ("Second half", predictions.iloc[midpoint:]),
    )
    rows: list[dict[str, Any]] = []
    for segment_name, segment in segments:
        actual = segment["actual"].to_numpy(dtype=float)
        scored: list[tuple[str, float, float]] = []
        for model, column in MODEL_PREDICTION_COLUMNS.items():
            if column not in segment:
                continue
            error = actual - segment[column].to_numpy(dtype=float)
            scored.append((model, float(np.mean(np.abs(error))), float(np.sqrt(np.mean(error**2)))))
        for rank, (model, mae, rmse) in enumerate(sorted(scored, key=lambda row: row[2]), start=1):
            rows.append(
                {
                    "test_segment": segment_name,
                    "start_date": str(pd.Timestamp(segment["date"].iloc[0]).date()),
                    "end_date": str(pd.Timestamp(segment["date"].iloc[-1]).date()),
                    "observations": len(segment),
                    "rank_by_RMSE": rank,
                    "model": model,
                    "MAE": f"{mae:.8f}",
                    "RMSE": f"{rmse:.8f}",
                }
            )
    return rows


def build_regime_performance_rows(predictions: pd.DataFrame) -> list[dict[str, Any]]:
    """Break test errors into low, medium and high realised-volatility regimes."""
    lower, upper = predictions["actual"].quantile([1 / 3, 2 / 3]).to_numpy(dtype=float)
    regimes = (
        ("Low", predictions["actual"] <= lower),
        ("Medium", (predictions["actual"] > lower) & (predictions["actual"] <= upper)),
        ("High", predictions["actual"] > upper),
    )
    rows: list[dict[str, Any]] = []
    for regime_name, mask in regimes:
        regime = predictions.loc[mask]
        actual = regime["actual"].to_numpy(dtype=float)
        scored: list[tuple[str, float, float, float]] = []
        for model, column in MODEL_PREDICTION_COLUMNS.items():
            if column not in regime:
                continue
            forecast = regime[column].to_numpy(dtype=float)
            error = forecast - actual
            scored.append(
                (
                    model,
                    float(np.mean(np.abs(error))),
                    float(np.sqrt(np.mean(error**2))),
                    float(np.mean(error)),
                )
            )
        for rank, (model, mae, rmse, bias) in enumerate(
            sorted(scored, key=lambda row: row[2]), start=1
        ):
            rows.append(
                {
                    "volatility_regime": regime_name,
                    "observations": len(regime),
                    "actual_min": f"{float(actual.min()):.8f}",
                    "actual_max": f"{float(actual.max()):.8f}",
                    "lower_tercile_threshold": f"{lower:.8f}",
                    "upper_tercile_threshold": f"{upper:.8f}",
                    "rank_by_RMSE": rank,
                    "model": model,
                    "MAE": f"{mae:.8f}",
                    "RMSE": f"{rmse:.8f}",
                    "mean_prediction_bias": f"{bias:.8f}",
                }
            )
    return rows


def build_permutation_importance_rows(
    model: Any,
    x_test: np.ndarray,
    y_test: np.ndarray,
    feature_names: tuple[str, ...],
    random_seed: int,
    repeats: int = 10,
) -> list[dict[str, Any]]:
    """Measure test RMSE increase when one feature is independently shuffled."""
    if repeats < 1:
        raise ValueError("Permutation-importance repeats must be positive")
    baseline = model.predict(x_test)
    baseline_rmse = float(np.sqrt(np.mean((y_test - baseline) ** 2)))
    rng = np.random.default_rng(random_seed)
    rows: list[dict[str, Any]] = []
    for feature_index, feature in enumerate(feature_names):
        increases: list[float] = []
        for _ in range(repeats):
            permuted = x_test.copy()
            permuted[:, feature_index] = rng.permutation(permuted[:, feature_index])
            permuted_prediction = model.predict(permuted)
            permuted_rmse = float(np.sqrt(np.mean((y_test - permuted_prediction) ** 2)))
            increases.append(permuted_rmse - baseline_rmse)
        rows.append(
            {
                "feature": feature,
                "baseline_RMSE": f"{baseline_rmse:.8f}",
                "mean_RMSE_increase": f"{float(np.mean(increases)):.8f}",
                "std_RMSE_increase": f"{float(np.std(increases, ddof=1)):.8f}" if repeats > 1 else "0.00000000",
                "repeats": repeats,
                "interpretation_note": "Positive values mean shuffling the feature worsened test RMSE; this is predictive association, not causality.",
            }
        )
    return sorted(rows, key=lambda row: float(row["mean_RMSE_increase"]), reverse=True)


def build_block_bootstrap_rows(
    predictions: pd.DataFrame,
    random_seed: int,
    samples: int = 2000,
    block_length: int = 30,
) -> list[dict[str, Any]]:
    """Paired circular moving-block bootstrap for RMSE differences vs rolling."""
    if samples < 1 or block_length < 2:
        raise ValueError("Bootstrap samples and block length must be positive")
    n_obs = len(predictions)
    if n_obs < block_length:
        raise ValueError("Bootstrap block length cannot exceed the prediction sample")

    rng = np.random.default_rng(random_seed)
    blocks_per_sample = int(np.ceil(n_obs / block_length))
    actual = predictions["actual"].to_numpy(dtype=float)
    rolling = predictions["rolling_historical"].to_numpy(dtype=float)
    rolling_rmse = float(np.sqrt(np.mean((actual - rolling) ** 2)))
    rows: list[dict[str, Any]] = []

    for model, column in MODEL_PREDICTION_COLUMNS.items():
        if column not in predictions:
            continue
        forecast = predictions[column].to_numpy(dtype=float)
        point_rmse = float(np.sqrt(np.mean((actual - forecast) ** 2)))
        differences = np.empty(samples, dtype=float)
        for sample_index in range(samples):
            starts = rng.integers(0, n_obs, size=blocks_per_sample)
            indices = np.concatenate(
                [(start + np.arange(block_length)) % n_obs for start in starts]
            )[:n_obs]
            sampled_actual = actual[indices]
            sampled_rolling = rolling[indices]
            sampled_forecast = forecast[indices]
            sampled_rolling_rmse = float(
                np.sqrt(np.mean((sampled_actual - sampled_rolling) ** 2))
            )
            sampled_model_rmse = float(
                np.sqrt(np.mean((sampled_actual - sampled_forecast) ** 2))
            )
            differences[sample_index] = sampled_model_rmse - sampled_rolling_rmse

        lower, median, upper = np.quantile(differences, [0.025, 0.5, 0.975])
        rows.append(
            {
                "model": model,
                "RMSE": f"{point_rmse:.8f}",
                "rolling_RMSE": f"{rolling_rmse:.8f}",
                "RMSE_difference_vs_rolling": f"{point_rmse - rolling_rmse:.8f}",
                "bootstrap_median_difference": f"{median:.8f}",
                "bootstrap_95pct_lower": f"{lower:.8f}",
                "bootstrap_95pct_upper": f"{upper:.8f}",
                "bootstrap_share_better_than_rolling": f"{float(np.mean(differences < 0.0)):.4f}",
                "bootstrap_samples": samples,
                "block_length_days": block_length,
                "method_note": "Paired circular moving-block bootstrap; negative RMSE difference favours the model over rolling.",
            }
        )
    return rows
