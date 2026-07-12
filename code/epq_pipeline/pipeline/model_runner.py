"""CLI orchestration for the modelling pipeline."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from epq_pipeline.common.io import ensure_directory, write_csv_rows, write_json, write_text
from epq_pipeline.common.types import PerformanceRow
from epq_pipeline.config import ModelRunConfig
from epq_pipeline.features.engineering import (
    add_base_features,
    apply_standardization,
    build_lstm_sequences,
    build_modelling_frame,
    chronological_split,
    fit_standardization_stats,
    load_dataset,
)
from epq_pipeline.models.garch import fit_garch_grid, garch_realised_vol_forecast
from epq_pipeline.models.linear import (
    LinearRegressionArtifacts,
    coefficient_rows,
    fit_linear_regression,
    predict_linear_regression,
)
from epq_pipeline.models.lstm import (
    LSTMTrainingArtifacts,
    fit_lstm_model,
    predict_lstm_model,
    skipped_lstm_artifacts,
    torch_is_available,
)
from epq_pipeline.models.metrics import performance_row, rank_performance_rows
from epq_pipeline.models.random_forest import SimpleRandomForestRegressor
from epq_pipeline.reporting.charting import draw_forecast_chart
from epq_pipeline.reporting.exports import build_model_summary_markdown, build_run_metadata


@dataclass
class PreparedModelData:
    raw_dataset: pd.DataFrame
    featured_dataset: pd.DataFrame
    frame: pd.DataFrame
    train: pd.DataFrame
    test: pd.DataFrame
    x_train_scaled: np.ndarray
    x_test_scaled: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray


@dataclass
class LSTMPipelineResult:
    artifacts: LSTMTrainingArtifacts
    predictions: np.ndarray | None


def build_arg_parser() -> argparse.ArgumentParser:
    default_config = ModelRunConfig()
    parser = argparse.ArgumentParser(description="Run the EPQ volatility model comparison pipeline.")
    parser.add_argument("--input-path", default=str(default_config.input_path), help="Processed volatility CSV input path")
    parser.add_argument("--output-dir", default=str(default_config.output_dir), help="Directory for model outputs")
    return parser


def config_from_args(args: argparse.Namespace) -> ModelRunConfig:
    return ModelRunConfig(
        input_path=Path(args.input_path),
        output_dir=Path(args.output_dir),
    )


def export_lstm_history(path: Path, history_rows: list[dict[str, float]]) -> None:
    if not history_rows:
        history_rows = [{"epoch": 0, "train_mse_on_scaled_target": "", "validation_mse_on_scaled_target": ""}]
    write_csv_rows(
        path,
        ["epoch", "train_mse_on_scaled_target", "validation_mse_on_scaled_target"],
        history_rows,
    )


def prepare_modelling_data(config: ModelRunConfig) -> PreparedModelData:
    raw_dataset = load_dataset(config.input_path, config.rv_col)
    featured_dataset = add_base_features(raw_dataset, config.rv_col, config.target_col)
    frame = build_modelling_frame(featured_dataset, config.feature_cols, config.target_col)
    split = chronological_split(frame, config.train_fraction)
    train = split.train
    test = split.test

    x_train = train[list(config.feature_cols)].to_numpy(dtype=float)
    y_train = train[config.target_col].to_numpy(dtype=float)
    x_test = test[list(config.feature_cols)].to_numpy(dtype=float)
    y_test = test[config.target_col].to_numpy(dtype=float)

    scaling = fit_standardization_stats(x_train)
    return PreparedModelData(
        raw_dataset=raw_dataset,
        featured_dataset=featured_dataset,
        frame=frame,
        train=train,
        test=test,
        x_train_scaled=apply_standardization(x_train, scaling),
        x_test_scaled=apply_standardization(x_test, scaling),
        y_train=y_train,
        y_test=y_test,
    )


def build_garch_predictions(prepared: PreparedModelData) -> tuple[dict[str, Any], np.ndarray]:
    training_end_date = prepared.train["date"].iloc[-1]
    garch_train_returns = prepared.raw_dataset[prepared.raw_dataset["date"] <= training_end_date]["log_return"].dropna().to_numpy(dtype=float)
    garch_params = fit_garch_grid(garch_train_returns)
    prepared.featured_dataset["garch_1_1"] = garch_realised_vol_forecast(prepared.featured_dataset, garch_params)
    garch_pred = prepared.featured_dataset.loc[prepared.test.index, "garch_1_1"].to_numpy(dtype=float)
    return garch_params, garch_pred


def annotate_lstm_metadata(
    artifacts: LSTMTrainingArtifacts,
    sequence_map: dict[str, np.ndarray],
    config: ModelRunConfig,
) -> None:
    artifacts.metadata["sequence_features"] = list(config.lstm_feature_cols)
    if len(sequence_map["dates_train"]) > 0:
        artifacts.metadata["train_sequence_start_date"] = str(pd.Timestamp(sequence_map["dates_train"][0]).date())
        artifacts.metadata["train_sequence_end_date"] = str(pd.Timestamp(sequence_map["dates_train"][-1]).date())
        artifacts.metadata["train_sequences_total"] = int(len(sequence_map["x_train"]))
    if len(sequence_map["dates_test"]) > 0:
        artifacts.metadata["test_sequence_start_date"] = str(pd.Timestamp(sequence_map["dates_test"][0]).date())
        artifacts.metadata["test_sequence_end_date"] = str(pd.Timestamp(sequence_map["dates_test"][-1]).date())
        artifacts.metadata["test_sequences"] = int(len(sequence_map["x_test"]))


def build_lstm_result(prepared: PreparedModelData, config: ModelRunConfig) -> LSTMPipelineResult:
    if not torch_is_available():
        return LSTMPipelineResult(
            artifacts=skipped_lstm_artifacts("PyTorch is not available in the current Python environment."),
            predictions=None,
        )

    lstm_train_values = prepared.train[list(config.lstm_feature_cols)].to_numpy(dtype=float)
    lstm_scaling = fit_standardization_stats(lstm_train_values)
    full_lstm_values = prepared.frame[list(config.lstm_feature_cols)].to_numpy(dtype=float)
    full_lstm_scaled = apply_standardization(full_lstm_values, lstm_scaling)
    sequence_map = build_lstm_sequences(
        features=full_lstm_scaled,
        targets=prepared.frame[config.target_col].to_numpy(dtype=float),
        dates=prepared.frame["date"].to_numpy(),
        split_index=len(prepared.train),
        sequence_length=config.lstm.sequence_length,
    )

    artifacts = fit_lstm_model(
        x_train=sequence_map["x_train"],
        y_train=sequence_map["y_train"],
        config=config.lstm,
        random_seed=config.random_seed,
    )
    annotate_lstm_metadata(artifacts, sequence_map, config)

    if artifacts.model is None or len(sequence_map["x_test"]) == 0:
        return LSTMPipelineResult(artifacts=artifacts, predictions=None)

    predictions = predict_lstm_model(
        artifacts,
        sequence_map["x_test"],
        target_mean=float(artifacts.metadata["target_mean"]),
        target_std=float(artifacts.metadata["target_std"]),
    )
    return LSTMPipelineResult(artifacts=artifacts, predictions=predictions)


def build_predictions_frame(
    prepared: PreparedModelData,
    garch_pred: np.ndarray,
    linear_pred: np.ndarray,
    random_forest_pred: np.ndarray,
    lstm_pred: np.ndarray | None,
    config: ModelRunConfig,
) -> pd.DataFrame:
    predictions = pd.DataFrame(
        {
            "date": prepared.test["date"].to_numpy(),
            "actual": prepared.y_test,
            "rolling_historical": prepared.test[config.rv_col].to_numpy(dtype=float),
            "garch_1_1": garch_pred,
            "lagged_linear_regression": linear_pred,
            "random_forest": random_forest_pred,
        }
    )
    if lstm_pred is not None:
        predictions["lstm"] = lstm_pred
    return predictions


def build_performance_rows(predictions: pd.DataFrame, y_test: np.ndarray) -> list[PerformanceRow]:
    rows: list[PerformanceRow] = [
        performance_row("Rolling historical volatility", "Benchmark", y_test, predictions["rolling_historical"].to_numpy(dtype=float)),
        performance_row("GARCH(1,1)", "Traditional statistical", y_test, predictions["garch_1_1"].to_numpy(dtype=float)),
        performance_row("Lagged linear regression", "Interpretable lag-feature model", y_test, predictions["lagged_linear_regression"].to_numpy(dtype=float)),
        performance_row("Random Forest", "Machine learning", y_test, predictions["random_forest"].to_numpy(dtype=float)),
    ]
    if "lstm" in predictions:
        rows.append(performance_row("LSTM", "Machine learning", y_test, predictions["lstm"].to_numpy(dtype=float)))
    return rank_performance_rows(rows)


def export_model_outputs(
    config: ModelRunConfig,
    prepared: PreparedModelData,
    predictions: pd.DataFrame,
    ranked_rows: list[PerformanceRow],
    random_forest: SimpleRandomForestRegressor,
    linear_artifacts: LinearRegressionArtifacts,
    garch_params: dict[str, Any],
    lstm_artifacts: LSTMTrainingArtifacts,
) -> list[Path]:
    predictions.to_csv(config.predictions_path, index=False, lineterminator="\n", date_format="%Y-%m-%d")
    write_csv_rows(
        config.performance_path,
        ["rank_by_RMSE", "model", "category", "MAE", "MSE", "RMSE"],
        [row.as_csv_row(rank) for rank, row in enumerate(ranked_rows, start=1)],
    )

    importances = random_forest.feature_importances_ if random_forest.feature_importances_ is not None else np.zeros(len(config.feature_cols))
    feature_rows = [
        {"feature": feature, "importance": f"{importance:.8f}"}
        for feature, importance in sorted(zip(config.feature_cols, importances), key=lambda item: item[1], reverse=True)
    ]
    write_csv_rows(config.feature_importance_path, ["feature", "importance"], feature_rows)
    write_csv_rows(config.linear_coefficients_path, ["term", "coefficient"], coefficient_rows(linear_artifacts))
    write_json(config.garch_path, garch_params)
    write_json(config.lstm_summary_path, lstm_artifacts.metadata)
    export_lstm_history(config.lstm_history_path, lstm_artifacts.history_rows)
    write_json(
        config.run_metadata_path,
        build_run_metadata(
            config,
            prepared.raw_dataset,
            prepared.frame,
            prepared.train,
            prepared.test,
            garch_params,
            lstm_artifacts.metadata,
        ),
    )
    draw_forecast_chart(predictions, config.chart_path)
    write_text(
        config.summary_path,
        build_model_summary_markdown(
            config,
            prepared.frame,
            prepared.train,
            prepared.test,
            ranked_rows,
            lstm_artifacts.metadata,
        ),
    )
    return [
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
    ]


def run_model_pipeline(config: ModelRunConfig) -> list[Path]:
    ensure_directory(config.output_dir)
    prepared = prepare_modelling_data(config)
    garch_params, garch_pred = build_garch_predictions(prepared)

    linear_artifacts = fit_linear_regression(prepared.x_train_scaled, prepared.y_train, config.feature_cols)
    linear_pred = predict_linear_regression(prepared.x_test_scaled, linear_artifacts)

    random_forest = SimpleRandomForestRegressor(config.random_forest, random_state=config.random_seed).fit(
        prepared.x_train_scaled,
        prepared.y_train,
    )
    random_forest_pred = random_forest.predict(prepared.x_test_scaled)

    lstm_result = build_lstm_result(prepared, config)
    predictions = build_predictions_frame(
        prepared,
        garch_pred,
        linear_pred,
        random_forest_pred,
        lstm_result.predictions,
        config,
    )
    ranked_rows = build_performance_rows(predictions, prepared.y_test)
    return export_model_outputs(
        config,
        prepared,
        predictions,
        ranked_rows,
        random_forest,
        linear_artifacts,
        garch_params,
        lstm_result.artifacts,
    )


def run_model_command(args: argparse.Namespace) -> int:
    written_paths = run_model_pipeline(config_from_args(args))
    for path in written_paths:
        print(f"Wrote {path}")
    return 0


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    return run_model_command(args)


if __name__ == "__main__":
    raise SystemExit(main())
