"""Structured evidence for comparison beyond forecast-error metrics."""

from __future__ import annotations

from typing import Any

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
        "explanation_evidence": "Omega, alpha, and beta separately represent baseline variance, shock response, and persistence.",
        "interpretability_limit": "Conversion from one-day conditional variance to rolling realised volatility adds an indirect step.",
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
        "explanation_evidence": "Exported impurity-based feature importance identifies the variables used across the forest.",
        "interpretability_limit": "Global feature importance does not explain the direction or one individual prediction.",
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
