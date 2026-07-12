"""Markdown and metadata exporters."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pandas as pd

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
        "- Validation: fixed chronological 80/20 holdout; no random shuffling and no walk-forward refitting",
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
            f"- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting, then converted into a {config.rv_window}-day realised-volatility forecast using recent observed returns plus the one-step-ahead conditional variance.",
            "- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.",
        ]
    )

    if lstm_metadata.get("status") == "trained":
        lines.append(
            f"- LSTM is fitted using PyTorch on rolling {config.lstm.sequence_length}-day sequences of core market features. Early stopping selected epoch {lstm_metadata['epochs_trained']} using a chronological validation split."
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

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- `{config.performance_path}`",
            f"- `{config.predictions_path}`",
            f"- `{config.feature_importance_path}`",
            f"- `{config.linear_coefficients_path}`",
            f"- `{config.garch_path}`",
            f"- `{config.lstm_summary_path}`",
            f"- `{config.lstm_history_path}`",
            f"- `{config.computational_profile_path}`",
            f"- `{config.multidimensional_comparison_path}`",
            f"- `{config.robustness_path}`",
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
) -> dict[str, Any]:
    return to_jsonable(
        {
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "input_path": config.input_path,
            "output_dir": config.output_dir,
            "feature_columns": config.feature_cols,
            "lstm_feature_columns": config.lstm_feature_cols,
            "train_fraction": config.train_fraction,
            "validation_design": "fixed chronological holdout",
            "primary_volatility_window_days": config.rv_window,
            "robustness_windows_days": config.robustness_windows,
            "random_seed": config.random_seed,
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
                "start_date": str(test["date"].iloc[0].date()),
                "end_date": str(test["date"].iloc[-1].date()),
            },
            "random_forest_hyperparameters": config.random_forest,
            "lstm_hyperparameters": config.lstm,
            "garch_parameters": garch_params,
            "lstm_summary": lstm_metadata,
            "model_timings_seconds": timings or {},
            "model_complexities": complexities or {},
            "generated_outputs": [
                config.performance_path,
                config.predictions_path,
                config.feature_importance_path,
                config.linear_coefficients_path,
                config.garch_path,
                config.lstm_summary_path,
                config.lstm_history_path,
                config.computational_profile_path,
                config.multidimensional_comparison_path,
                config.robustness_path,
                config.run_metadata_path,
                config.chart_path,
                config.summary_path,
            ],
        }
    )
