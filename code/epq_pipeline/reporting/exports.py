"""Markdown and metadata exporters."""

from __future__ import annotations

import hashlib
import platform
import sys
from datetime import UTC, datetime
from typing import Any

import numpy as np
import pandas as pd
from PIL import __version__ as pillow_version

from epq_pipeline.common.io import to_jsonable
from epq_pipeline.common.types import PerformanceRow
from epq_pipeline.config import ModelRunConfig


def build_model_summary_markdown(
    config: ModelRunConfig,
    frame: pd.DataFrame,
    train: pd.DataFrame,
    test: pd.DataFrame,
    ranked_rows: list[PerformanceRow],
    lstm_metadata: dict[str, Any],
    computational_rows: list[dict[str, Any]] | None = None,
    robustness_rows: list[dict[str, Any]] | None = None,
    test_segment_rows: list[dict[str, Any]] | None = None,
    uncertainty_rows: list[dict[str, Any]] | None = None,
    regime_rows: list[dict[str, Any]] | None = None,
    walk_forward_rows: list[PerformanceRow] | None = None,
    lstm_seed_rows: list[dict[str, Any]] | None = None,
) -> str:
    best = ranked_rows[0]
    lines = [
        "# Current Volatility Model Results",
        "",
        f"Generated: {datetime.now(UTC).replace(microsecond=0).isoformat()}",
        "",
        "## Dataset",
        "",
        f"- Source file: `{config.input_path}`",
        f"- Model frame rows: {len(frame)}",
        f"- Train rows: {len(train)} ({train['date'].iloc[0].date()} to {train['date'].iloc[-1].date()})",
        f"- Test rows: {len(test)} ({test['date'].iloc[0].date()} to {test['date'].iloc[-1].date()})",
        f"- Forecast target: next-day {config.rv_window}-day realised volatility, not annualised",
        f"- Primary validation: frozen forecast-origin cutoff at {config.test_start_date}; later data extends the test set without moving earlier test rows into training",
        f"- Supplementary validation: {config.rolling_origin_folds}-fold expanding-window rolling-origin evaluation with refitting at each later boundary",
        "- Exported `date` is the forecast-origin date; `target_date` is the next completed candle whose updated rolling volatility is predicted",
        "",
        "## Result",
        "",
        f"Best current model by RMSE: **{best.model}** with RMSE `{best.rmse:.8f}`.",
        "",
        "| Rank | Model | Category | MAE | MSE | RMSE |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for rank, row in enumerate(ranked_rows, start=1):
        lines.append(
            f"| {rank} | {row.model} | {row.category} | {row.mae:.8f} | {row.mse:.8f} | {row.rmse:.8f} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Rolling historical volatility is the transparent benchmark.",
            f"- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting. The primary {config.rv_window}-day standard-deviation forecast is E[s], evaluated by 80-point Gauss-Hermite quadrature; sqrt(E[s^2]) is retained as a target-conversion sensitivity.",
            "- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.",
        ]
    )

    if lstm_metadata.get("status") == "trained":
        lines.append(
            f"- LSTM is fitted using PyTorch on rolling {config.lstm.sequence_length}-day sequences of core market features. Early stopping selected epoch {lstm_metadata.get('best_epoch', lstm_metadata['epochs_trained'])} from {lstm_metadata.get('epochs_run', 'the recorded')} completed epochs using a chronological validation split."
        )
    else:
        lines.append(f"- LSTM status: {lstm_metadata.get('reason', 'not available')}")

    if computational_rows:
        lines.extend(
            [
                "",
                "## Computational Practicality",
                "",
                "Timings are from one local CPU run and are implementation-specific, so they indicate relative project cost rather than universal benchmark speed.",
                "",
                "| Model | Fit seconds | Predict seconds | Complexity |",
                "| --- | --- | --- | --- |",
            ]
        )
        for row in computational_rows:
            lines.append(
                f"| {row['model']} | {row['fit_seconds']} | {row['predict_seconds']} | {row['complexity_value']} {row['complexity_measure']} |"
            )

    if robustness_rows:
        lines.extend(
            [
                "",
                "## Robustness Across Target Windows",
                "",
                "| Window | Rank | Model | RMSE | Difference from rolling benchmark |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in robustness_rows:
            lines.append(
                f"| {row['volatility_window_days']} days | {row['rank_by_RMSE']} | {row['model']} | {row['RMSE']} | {row['RMSE_vs_rolling_percent']}% |"
            )

    if test_segment_rows:
        lines.extend(
            [
                "",
                "## Robustness Across Test-Period Halves",
                "",
                "| Segment | Dates | Rank | Model | RMSE |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in test_segment_rows:
            lines.append(
                f"| {row['test_segment']} | {row['start_date']} to {row['end_date']} | {row['rank_by_RMSE']} | {row['model']} | {row['RMSE']} |"
            )

    if uncertainty_rows:
        lines.extend(
            [
                "",
                "## Moving-Block Bootstrap Versus Rolling",
                "",
                "Negative differences favour the model. Intervals use 2,000 paired circular resamples of 30-day blocks.",
                "",
                "| Model | RMSE difference | 95% interval |",
                "| --- | --- | --- |",
            ]
        )
        for row in uncertainty_rows:
            lines.append(
                f"| {row['model']} | {row['RMSE_difference_vs_rolling']} | [{row['bootstrap_95pct_lower']}, {row['bootstrap_95pct_upper']}] |"
            )

    if regime_rows:
        lines.extend(
            [
                "",
                "## Accuracy by Realised-Volatility Regime",
                "",
                "Regimes are test-target terciles. Bias is prediction minus actual; positive values indicate overprediction.",
                "",
                "| Regime | Rank | Model | RMSE | Bias |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in regime_rows:
            lines.append(
                f"| {row['volatility_regime']} | {row['rank_by_RMSE']} | {row['model']} | {row['RMSE']} | {row['mean_prediction_bias']} |"
            )

    if walk_forward_rows:
        lines.extend(
            [
                "",
                f"## Expanding-Window Rolling-Origin Evaluation ({config.rolling_origin_folds} Folds)",
                "",
                "Each fold refits on all information available before its test block. The first fold reuses the primary fitted models because its training boundary is identical.",
                "",
                "| Rank | Model | MAE | RMSE |",
                "| --- | --- | --- | --- |",
            ]
        )
        for rank, row in enumerate(walk_forward_rows, start=1):
            lines.append(f"| {rank} | {row.model} | {row.mae:.8f} | {row.rmse:.8f} |")

    if lstm_seed_rows:
        lines.extend(
            [
                "",
                "## LSTM Seed Stability",
                "",
                "| Seed | Best epoch | MAE | RMSE |",
                "| --- | --- | --- | --- |",
            ]
        )
        for row in lstm_seed_rows:
            lines.append(
                f"| {row['seed']} | {row['best_epoch']} | {row['MAE']} | {row['RMSE']} |"
            )

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- `{config.performance_path}`",
            f"- `{config.predictions_path}`",
            f"- `{config.feature_importance_path}`",
            f"- `{config.rf_permutation_importance_path}`",
            f"- `{config.rf_oob_path}`",
            f"- `{config.linear_coefficients_path}`",
            f"- `{config.garch_path}`",
            f"- `{config.garch_conversion_sensitivity_path}`",
            f"- `{config.lstm_summary_path}`",
            f"- `{config.lstm_history_path}`",
            f"- `{config.computational_profile_path}`",
            f"- `{config.multidimensional_comparison_path}`",
            f"- `{config.robustness_path}`",
            f"- `{config.test_segment_path}`",
            f"- `{config.uncertainty_path}`",
            f"- `{config.regime_performance_path}`",
            f"- `{config.walk_forward_performance_path}`",
            f"- `{config.walk_forward_fold_path}`",
            f"- `{config.walk_forward_predictions_path}`",
            f"- `{config.lstm_seed_stability_path}`",
            f"- `{config.run_metadata_path}`",
            f"- `{config.chart_path}`",
            f"- `{config.summary_path}`",
        ]
    )
    return "\n".join(lines) + "\n"


def build_run_metadata(
    config: ModelRunConfig,
    raw_dataset: pd.DataFrame,
    frame: pd.DataFrame,
    train: pd.DataFrame,
    test: pd.DataFrame,
    garch_params: dict[str, Any],
    lstm_metadata: dict[str, Any],
    timings: dict[str, dict[str, float]] | None = None,
    complexities: dict[str, dict[str, Any]] | None = None,
    resolved_rf_max_features: int | None = None,
) -> dict[str, Any]:
    input_sha256 = None
    input_bytes = None
    if config.input_path.exists():
        input_sha256 = hashlib.sha256(config.input_path.read_bytes()).hexdigest()
        input_bytes = config.input_path.stat().st_size

    lstm_fit_sequences = lstm_metadata.get("train_sequences")
    lstm_validation_sequences = lstm_metadata.get("validation_sequences")
    lstm_total_sequences = lstm_metadata.get("train_sequences_total")
    return to_jsonable(
        {
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "input_path": config.input_path,
            "output_dir": config.output_dir,
            "feature_columns": config.feature_cols,
            "lstm_feature_columns": config.lstm_feature_cols,
            "split_cutoff": config.test_start_date,
            "validation_design": "frozen forecast-origin cutoff",
            "split_note": "The cutoff was initially chosen near an 80/20 division; subsequent refreshes only extend the test period.",
            "supplementary_validation_design": "expanding-window rolling-origin evaluation",
            "primary_volatility_window_days": config.rv_window,
            "robustness_windows_days": config.robustness_windows,
            "rolling_origin_folds": config.rolling_origin_folds,
            "lstm_stability_seeds": config.lstm_stability_seeds,
            "random_seed": config.random_seed,
            "processed_input": {
                "path": config.input_path,
                "sha256": input_sha256,
                "bytes": input_bytes,
            },
            "runtime_versions": {
                "python": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "pandas": pd.__version__,
                "pillow": pillow_version,
                "torch": lstm_metadata.get("torch_version"),
                "python_executable": sys.executable,
            },
            "raw_dataset": {
                "rows": len(raw_dataset),
                "start_date": str(raw_dataset["date"].iloc[0].date()),
                "end_date": str(raw_dataset["date"].iloc[-1].date()),
            },
            "modelling_frame": {
                "rows": len(frame),
                "start_date": str(frame["date"].iloc[0].date()),
                "end_date": str(frame["date"].iloc[-1].date()),
            },
            "train_window": {
                "rows": len(train),
                "start_date": str(train["date"].iloc[0].date()),
                "end_date": str(train["date"].iloc[-1].date()),
            },
            "test_window": {
                "rows": len(test),
                "forecast_origin_start_date": str(test["date"].iloc[0].date()),
                "forecast_origin_end_date": str(test["date"].iloc[-1].date()),
                "target_start_date": str(test["target_date"].iloc[0].date()),
                "target_end_date": str(test["target_date"].iloc[-1].date()),
            },
            "random_forest_hyperparameters": {
                "configured": config.random_forest,
                "resolved_max_features": resolved_rf_max_features,
                "max_features_resolution_note": "A null configured value resolves to floor(sqrt(feature_count)), with a minimum of one.",
            },
            "lstm_hyperparameters": config.lstm,
            "garch_parameters": garch_params,
            "lstm_summary": lstm_metadata,
            "model_timings_seconds": timings or {},
            "model_complexities": complexities or {},
            "effective_training_samples": {
                "Rolling historical volatility": {
                    "fitted_rows": 0,
                    "note": "Persistence benchmark; no parameters are fitted.",
                },
                "GARCH(1,1)": {
                    "finite_return_rows": garch_params.get("training_observations"),
                },
                "Lagged linear regression": {
                    "frame_rows": len(train),
                },
                "Random Forest": {
                    "frame_rows": len(train),
                },
                "LSTM": {
                    "parameter_fit_sequences": lstm_fit_sequences,
                    "validation_sequences": lstm_validation_sequences,
                    "total_pretest_sequences": lstm_total_sequences,
                },
            },
            "generated_outputs": [
                config.performance_path,
                config.predictions_path,
                config.feature_importance_path,
                config.rf_permutation_importance_path,
                config.rf_oob_path,
                config.linear_coefficients_path,
                config.garch_path,
                config.garch_conversion_sensitivity_path,
                config.lstm_summary_path,
                config.lstm_history_path,
                config.computational_profile_path,
                config.multidimensional_comparison_path,
                config.robustness_path,
                config.test_segment_path,
                config.uncertainty_path,
                config.regime_performance_path,
                config.walk_forward_performance_path,
                config.walk_forward_fold_path,
                config.walk_forward_predictions_path,
                config.lstm_seed_stability_path,
                config.run_metadata_path,
                config.chart_path,
                config.summary_path,
            ],
        }
    )
