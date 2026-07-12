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
        "- Forecast target: next-day 30-day realised volatility, not annualised",
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
            "- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting, then converted into a 30-day realised-volatility forecast using the most recent 29 observed returns plus the one-step-ahead conditional variance.",
            "- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.",
        ]
    )

    if lstm_metadata.get("status") == "trained":
        lines.append(
            f"- LSTM is fitted using PyTorch on rolling {config.lstm.sequence_length}-day sequences of core market features. Early stopping selected epoch {lstm_metadata['epochs_trained']} using a chronological validation split."
        )
    else:
        lines.append(f"- LSTM status: {lstm_metadata.get('reason', 'not available')}")

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
) -> dict[str, Any]:
    return to_jsonable(
        {
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "input_path": config.input_path,
            "output_dir": config.output_dir,
            "feature_columns": config.feature_cols,
            "lstm_feature_columns": config.lstm_feature_cols,
            "train_fraction": config.train_fraction,
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
            "generated_outputs": [
                config.performance_path,
                config.predictions_path,
                config.feature_importance_path,
                config.linear_coefficients_path,
                config.garch_path,
                config.lstm_summary_path,
                config.lstm_history_path,
                config.run_metadata_path,
                config.chart_path,
                config.summary_path,
            ],
        }
    )
