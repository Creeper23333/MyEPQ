"""CLI orchestration for the modelling and evaluation pipeline."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from pathlib import Path
from time import perf_counter
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
    chronological_split_by_date,
    ensure_realised_volatility,
    fit_standardization_stats,
    load_dataset,
)
from epq_pipeline.models.garch import (
    GAUSS_HERMITE_NODE_COUNT,
    fit_garch_grid,
    garch_realised_vol_forecast,
    garch_realised_vol_rms_forecast,
)
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
    validation_count_for_sequence_count,
)
from epq_pipeline.models.metrics import performance_row, rank_performance_rows, regression_metrics
from epq_pipeline.models.random_forest import SimpleRandomForestRegressor
from epq_pipeline.reporting.charting import draw_forecast_chart
from epq_pipeline.reporting.evaluation import (
    build_block_bootstrap_rows,
    build_computational_rows,
    build_multidimensional_rows,
    build_permutation_importance_rows,
    build_regime_performance_rows,
    build_robustness_rows,
    build_test_segment_rows,
)
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
    fit_seconds: float
    predict_seconds: float


@dataclass
class ModelEvaluation:
    predictions: pd.DataFrame
    ranked_rows: list[PerformanceRow]
    garch_params: dict[str, Any]
    linear_artifacts: LinearRegressionArtifacts
    random_forest: SimpleRandomForestRegressor
    lstm_artifacts: LSTMTrainingArtifacts
    timings: dict[str, dict[str, float]]
    complexities: dict[str, dict[str, Any]]


@dataclass
class WalkForwardArtifacts:
    predictions: pd.DataFrame
    overall_rows: list[PerformanceRow]
    fold_rows: list[dict[str, Any]]


def assemble_prepared_data(
    raw_dataset: pd.DataFrame,
    featured_dataset: pd.DataFrame,
    frame: pd.DataFrame,
    train: pd.DataFrame,
    test: pd.DataFrame,
    config: ModelRunConfig,
) -> PreparedModelData:
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


def build_arg_parser() -> argparse.ArgumentParser:
    default_config = ModelRunConfig()
    parser = argparse.ArgumentParser(description="Run the EPQ volatility model comparison pipeline.")
    parser.add_argument("--input-path", default=str(default_config.input_path), help="Processed volatility CSV input path")
    parser.add_argument("--output-dir", default=str(default_config.output_dir), help="Directory for model outputs")
    parser.add_argument("--volatility-window", type=int, default=default_config.rv_window, help="Primary realised-volatility window")
    parser.add_argument(
        "--test-start-date",
        default=default_config.test_start_date,
        help="Fixed forecast-origin test start date in YYYY-MM-DD format",
    )
    return parser


def config_from_args(args: argparse.Namespace) -> ModelRunConfig:
    return ModelRunConfig(
        input_path=Path(args.input_path),
        output_dir=Path(args.output_dir),
        rv_window=args.volatility_window,
        test_start_date=args.test_start_date,
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
    raw_dataset = load_dataset(config.input_path, config.rv_col, config.rv_window)
    raw_dataset = ensure_realised_volatility(raw_dataset, config.rv_col, config.rv_window)
    featured_dataset = add_base_features(raw_dataset, config.rv_col, config.target_col)
    frame = build_modelling_frame(featured_dataset, config.feature_cols, config.target_col)
    split = chronological_split_by_date(frame, config.test_start_date)
    return assemble_prepared_data(
        raw_dataset,
        featured_dataset,
        frame,
        split.train,
        split.test,
        config,
    )


def prepare_modelling_partition(
    primary: PreparedModelData,
    config: ModelRunConfig,
    train_end: int,
    test_end: int,
) -> PreparedModelData:
    """Build an expanding-window fold without recomputing raw features."""
    if not (0 < train_end < test_end <= len(primary.frame)):
        raise ValueError("Invalid expanding-window train/test boundaries")
    frame = primary.frame.iloc[:test_end].copy()
    train = frame.iloc[:train_end].copy()
    test = frame.iloc[train_end:test_end].copy()
    return assemble_prepared_data(
        primary.raw_dataset,
        primary.featured_dataset,
        frame,
        train,
        test,
        config,
    )


def expanding_window_boundaries(
    total_rows: int,
    primary_train_rows: int,
    folds: int,
) -> list[tuple[int, int]]:
    """Return non-overlapping test blocks with an expanding training end."""
    test_count = total_rows - primary_train_rows
    if not (0 < primary_train_rows < total_rows):
        raise ValueError("Expanding-window boundaries need non-empty train and test periods")
    if folds < 2 or test_count < folds:
        raise ValueError("Rolling-origin evaluation needs at least two non-empty folds")
    fold_size = int(np.ceil(test_count / folds))
    boundaries: list[tuple[int, int]] = []
    for fold_index in range(folds):
        train_end = primary_train_rows + fold_index * fold_size
        if train_end >= total_rows:
            break
        boundaries.append((train_end, min(train_end + fold_size, total_rows)))
    if len(boundaries) != folds or any(test_end <= train_end for train_end, test_end in boundaries):
        raise ValueError("Could not construct the requested number of rolling-origin folds")
    return boundaries


def align_forecasts_by_date(
    source_dates: pd.Series,
    forecasts: pd.Series,
    target_dates: pd.Series,
) -> np.ndarray:
    if source_dates.duplicated().any():
        raise ValueError("Forecast source dates must be unique")
    forecasts_by_date = pd.Series(forecasts.to_numpy(), index=pd.to_datetime(source_dates))
    aligned = pd.to_datetime(target_dates).map(forecasts_by_date).to_numpy(dtype=float)
    if not np.all(np.isfinite(aligned)):
        raise ValueError("Forecasts contain missing values after date alignment")
    return aligned


def build_garch_predictions(
    prepared: PreparedModelData,
    config: ModelRunConfig,
) -> tuple[dict[str, Any], np.ndarray, np.ndarray, float, float]:
    training_end_date = prepared.train["date"].iloc[-1]
    garch_train_returns = prepared.raw_dataset[
        prepared.raw_dataset["date"] <= training_end_date
    ]["log_return"].dropna().to_numpy(dtype=float)

    fit_started = perf_counter()
    garch_params: dict[str, Any] = fit_garch_grid(garch_train_returns)
    garch_params["primary_target_conversion"] = "E[s]"
    garch_params["gauss_hermite_nodes"] = GAUSS_HERMITE_NODE_COUNT
    garch_params["sensitivity_target_conversion"] = "sqrt(E[s^2])"
    fit_seconds = perf_counter() - fit_started

    predict_started = perf_counter()
    garch_series = garch_realised_vol_forecast(prepared.featured_dataset, garch_params, window=config.rv_window)
    garch_rms_series = garch_realised_vol_rms_forecast(
        prepared.featured_dataset,
        garch_params,
        window=config.rv_window,
    )
    garch_pred = align_forecasts_by_date(
        prepared.featured_dataset["date"],
        garch_series,
        prepared.test["date"],
    )
    garch_rms_pred = align_forecasts_by_date(
        prepared.featured_dataset["date"],
        garch_rms_series,
        prepared.test["date"],
    )
    predict_seconds = perf_counter() - predict_started
    return garch_params, garch_pred, garch_rms_pred, fit_seconds, predict_seconds


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
            fit_seconds=0.0,
            predict_seconds=0.0,
        )

    fit_started = perf_counter()
    train_sequence_count = len(prepared.train) - config.lstm.sequence_length + 1
    validation_count = validation_count_for_sequence_count(train_sequence_count, config.lstm)
    fit_sequence_count = train_sequence_count - validation_count
    scaling_row_count = config.lstm.sequence_length + fit_sequence_count - 1
    lstm_train_values = prepared.train.iloc[:scaling_row_count][
        list(config.lstm_feature_cols)
    ].to_numpy(dtype=float)
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
    fit_seconds = perf_counter() - fit_started

    if artifacts.model is None or len(sequence_map["x_test"]) == 0:
        return LSTMPipelineResult(artifacts, None, fit_seconds, 0.0)

    predict_started = perf_counter()
    predictions = predict_lstm_model(
        artifacts,
        sequence_map["x_test"],
        target_mean=float(artifacts.metadata["target_mean"]),
        target_std=float(artifacts.metadata["target_std"]),
    )
    predict_seconds = perf_counter() - predict_started
    return LSTMPipelineResult(artifacts, predictions, fit_seconds, predict_seconds)


def build_predictions_frame(
    prepared: PreparedModelData,
    garch_pred: np.ndarray,
    garch_rms_pred: np.ndarray,
    linear_pred: np.ndarray,
    random_forest_pred: np.ndarray,
    lstm_pred: np.ndarray | None,
    config: ModelRunConfig,
) -> pd.DataFrame:
    predictions = pd.DataFrame(
        {
            "date": prepared.test["date"].to_numpy(),
            "target_date": prepared.test["target_date"].to_numpy(),
            "actual": prepared.y_test,
            "rolling_historical": prepared.test[config.rv_col].to_numpy(dtype=float),
            "garch_1_1": garch_pred,
            "garch_sqrt_expected_variance": garch_rms_pred,
            "lagged_linear_regression": linear_pred,
            "random_forest": random_forest_pred,
        }
    )
    if lstm_pred is not None:
        predictions["lstm"] = lstm_pred
    return predictions


def build_performance_rows(predictions: pd.DataFrame, y_test: np.ndarray) -> list[PerformanceRow]:
    rows = [
        performance_row("Rolling historical volatility", "Benchmark", y_test, predictions["rolling_historical"].to_numpy(dtype=float)),
        performance_row("GARCH(1,1)", "Traditional statistical", y_test, predictions["garch_1_1"].to_numpy(dtype=float)),
        performance_row("Lagged linear regression", "Interpretable lag-feature model", y_test, predictions["lagged_linear_regression"].to_numpy(dtype=float)),
        performance_row("Random Forest", "Machine learning", y_test, predictions["random_forest"].to_numpy(dtype=float)),
    ]
    if "lstm" in predictions:
        rows.append(performance_row("LSTM", "Machine learning", y_test, predictions["lstm"].to_numpy(dtype=float)))
    return rank_performance_rows(rows)


def evaluate_models(prepared: PreparedModelData, config: ModelRunConfig) -> ModelEvaluation:
    rolling_started = perf_counter()
    rolling_pred = prepared.test[config.rv_col].to_numpy(dtype=float).copy()
    rolling_predict_seconds = perf_counter() - rolling_started

    (
        garch_params,
        garch_pred,
        garch_rms_pred,
        garch_fit_seconds,
        garch_predict_seconds,
    ) = build_garch_predictions(prepared, config)

    linear_fit_started = perf_counter()
    linear_artifacts = fit_linear_regression(prepared.x_train_scaled, prepared.y_train, config.feature_cols)
    linear_fit_seconds = perf_counter() - linear_fit_started
    linear_predict_started = perf_counter()
    linear_pred = predict_linear_regression(prepared.x_test_scaled, linear_artifacts)
    linear_predict_seconds = perf_counter() - linear_predict_started

    forest_fit_started = perf_counter()
    random_forest = SimpleRandomForestRegressor(config.random_forest, random_state=config.random_seed).fit(
        prepared.x_train_scaled,
        prepared.y_train,
    )
    forest_fit_seconds = perf_counter() - forest_fit_started
    forest_predict_started = perf_counter()
    random_forest_pred = random_forest.predict(prepared.x_test_scaled)
    forest_predict_seconds = perf_counter() - forest_predict_started

    lstm_result = build_lstm_result(prepared, config)
    predictions = build_predictions_frame(
        prepared,
        garch_pred,
        garch_rms_pred,
        linear_pred,
        random_forest_pred,
        lstm_result.predictions,
        config,
    )
    predictions["rolling_historical"] = rolling_pred
    ranked_rows = build_performance_rows(predictions, prepared.y_test)

    timings = {
        "Rolling historical volatility": {"fit_seconds": 0.0, "predict_seconds": rolling_predict_seconds},
        "GARCH(1,1)": {"fit_seconds": garch_fit_seconds, "predict_seconds": garch_predict_seconds},
        "Lagged linear regression": {"fit_seconds": linear_fit_seconds, "predict_seconds": linear_predict_seconds},
        "Random Forest": {"fit_seconds": forest_fit_seconds, "predict_seconds": forest_predict_seconds},
    }
    complexities: dict[str, dict[str, Any]] = {
        "Rolling historical volatility": {"measure": "fitted parameters", "value": 0},
        "GARCH(1,1)": {"measure": "fitted parameters", "value": 3},
        "Lagged linear regression": {"measure": "coefficients including intercept", "value": len(linear_artifacts.coefficients)},
        "Random Forest": {"measure": "tree nodes across forest", "value": random_forest.node_count},
    }
    if lstm_result.predictions is not None:
        timings["LSTM"] = {
            "fit_seconds": lstm_result.fit_seconds,
            "predict_seconds": lstm_result.predict_seconds,
        }
        complexities["LSTM"] = {
            "measure": "trainable parameters",
            "value": int(lstm_result.artifacts.metadata["trainable_parameter_count"]),
        }

    return ModelEvaluation(
        predictions=predictions,
        ranked_rows=ranked_rows,
        garch_params=garch_params,
        linear_artifacts=linear_artifacts,
        random_forest=random_forest,
        lstm_artifacts=lstm_result.artifacts,
        timings=timings,
        complexities=complexities,
    )


def run_robustness_checks(
    config: ModelRunConfig,
    primary_prepared: PreparedModelData,
    primary_evaluation: ModelEvaluation,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for window in sorted(set(config.robustness_windows)):
        if window == config.rv_window:
            prepared = primary_prepared
            evaluation = primary_evaluation
        else:
            robustness_config = replace(config, rv_window=window)
            prepared = prepare_modelling_data(robustness_config)
            evaluation = evaluate_models(prepared, robustness_config)
        rows.extend(
            build_robustness_rows(
                window=window,
                ranked_rows=evaluation.ranked_rows,
                train_start=str(prepared.train["date"].iloc[0].date()),
                train_end=str(prepared.train["date"].iloc[-1].date()),
                test_start=str(prepared.test["date"].iloc[0].date()),
                test_end=str(prepared.test["date"].iloc[-1].date()),
            )
        )
    return rows


def run_walk_forward_checks(
    config: ModelRunConfig,
    primary_prepared: PreparedModelData,
    primary_evaluation: ModelEvaluation,
) -> WalkForwardArtifacts:
    """Evaluate four expanding-window forecast blocks across the fixed holdout."""
    folds = config.rolling_origin_folds
    boundaries = expanding_window_boundaries(
        total_rows=len(primary_prepared.frame),
        primary_train_rows=len(primary_prepared.train),
        folds=folds,
    )
    prediction_frames: list[pd.DataFrame] = []
    fold_rows: list[dict[str, Any]] = []

    for fold_index, (train_end, test_end) in enumerate(boundaries):
        if fold_index == 0:
            fold_prepared = primary_prepared
            evaluation = primary_evaluation
            fold_predictions = evaluation.predictions.iloc[: test_end - train_end].copy()
        else:
            fold_prepared = prepare_modelling_partition(
                primary_prepared,
                config,
                train_end=train_end,
                test_end=test_end,
            )
            evaluation = evaluate_models(fold_prepared, config)
            fold_predictions = evaluation.predictions.copy()

        fold_number = fold_index + 1
        fold_predictions.insert(0, "walk_forward_fold", fold_number)
        fold_predictions.insert(1, "fit_train_end", str(fold_prepared.train["date"].iloc[-1].date()))
        prediction_frames.append(fold_predictions)

        ranked = build_performance_rows(
            fold_predictions,
            fold_predictions["actual"].to_numpy(dtype=float),
        )
        for rank, result in enumerate(ranked, start=1):
            fold_rows.append(
                {
                    "walk_forward_fold": fold_number,
                    "train_rows": len(fold_prepared.train),
                    "train_start": str(fold_prepared.train["date"].iloc[0].date()),
                    "train_end": str(fold_prepared.train["date"].iloc[-1].date()),
                    "test_start": str(fold_predictions["date"].iloc[0].date()),
                    "test_end": str(fold_predictions["date"].iloc[-1].date()),
                    "target_start": str(fold_predictions["target_date"].iloc[0].date()),
                    "target_end": str(fold_predictions["target_date"].iloc[-1].date()),
                    "test_rows": len(fold_predictions),
                    "rank_by_RMSE": rank,
                    "model": result.model,
                    "MAE": f"{result.mae:.8f}",
                    "MSE": f"{result.mse:.8f}",
                    "RMSE": f"{result.rmse:.8f}",
                }
            )

    predictions = pd.concat(prediction_frames, ignore_index=True)
    overall_rows = build_performance_rows(
        predictions,
        predictions["actual"].to_numpy(dtype=float),
    )
    return WalkForwardArtifacts(predictions, overall_rows, fold_rows)


def build_lstm_seed_stability_rows(
    prepared: PreparedModelData,
    evaluation: ModelEvaluation,
    config: ModelRunConfig,
) -> list[dict[str, Any]]:
    """Rerun the LSTM across fixed seeds without changing the final test set."""
    rows: list[dict[str, Any]] = []
    for seed in config.lstm_stability_seeds:
        if seed == config.random_seed and "lstm" in evaluation.predictions:
            artifacts = evaluation.lstm_artifacts
            predictions = evaluation.predictions["lstm"].to_numpy(dtype=float)
            fit_seconds = evaluation.timings["LSTM"]["fit_seconds"]
            predict_seconds = evaluation.timings["LSTM"]["predict_seconds"]
        else:
            result = build_lstm_result(prepared, replace(config, random_seed=seed))
            artifacts = result.artifacts
            predictions = result.predictions
            fit_seconds = result.fit_seconds
            predict_seconds = result.predict_seconds

        status = str(artifacts.metadata.get("status", "unknown"))
        if predictions is None:
            rows.append(
                {
                    "seed": seed,
                    "status": status,
                    "best_epoch": "",
                    "best_validation_mse_on_scaled_target": "",
                    "fit_seconds": f"{fit_seconds:.6f}",
                    "predict_seconds": f"{predict_seconds:.6f}",
                    "MAE": "",
                    "MSE": "",
                    "RMSE": "",
                }
            )
            continue
        metrics = regression_metrics(prepared.y_test, predictions)
        rows.append(
            {
                "seed": seed,
                "status": status,
                    "best_epoch": artifacts.metadata.get(
                        "best_epoch", artifacts.metadata.get("epochs_trained", "")
                    ),
                "best_validation_mse_on_scaled_target": artifacts.metadata.get(
                    "best_validation_mse_on_scaled_target", ""
                ),
                "fit_seconds": f"{fit_seconds:.6f}",
                "predict_seconds": f"{predict_seconds:.6f}",
                "MAE": f"{metrics['MAE']:.8f}",
                "MSE": f"{metrics['MSE']:.8f}",
                "RMSE": f"{metrics['RMSE']:.8f}",
            }
        )
    return rows


def export_model_outputs(
    config: ModelRunConfig,
    prepared: PreparedModelData,
    evaluation: ModelEvaluation,
    robustness_rows: list[dict[str, Any]],
    walk_forward: WalkForwardArtifacts,
    lstm_seed_rows: list[dict[str, Any]],
) -> list[Path]:
    evaluation.predictions.to_csv(config.predictions_path, index=False, lineterminator="\n", date_format="%Y-%m-%d")
    write_csv_rows(
        config.performance_path,
        ["rank_by_RMSE", "model", "category", "MAE", "MSE", "RMSE"],
        [row.as_csv_row(rank) for rank, row in enumerate(evaluation.ranked_rows, start=1)],
    )

    importances = evaluation.random_forest.feature_importances_
    if importances is None:
        importances = np.zeros(len(config.feature_cols))
    feature_rows = [
        {"feature": feature, "importance": f"{importance:.8f}"}
        for feature, importance in sorted(zip(config.feature_cols, importances), key=lambda item: item[1], reverse=True)
    ]
    write_csv_rows(config.feature_importance_path, ["feature", "importance"], feature_rows)
    permutation_rows = build_permutation_importance_rows(
        evaluation.random_forest,
        prepared.x_test_scaled,
        prepared.y_test,
        config.feature_cols,
        random_seed=config.random_seed,
    )
    write_csv_rows(
        config.rf_permutation_importance_path,
        [
            "feature", "baseline_RMSE", "mean_RMSE_increase", "std_RMSE_increase",
            "repeats", "interpretation_note",
        ],
        permutation_rows,
    )
    write_json(
        config.rf_oob_path,
        {
            "training_rows": len(prepared.train),
            "oob_rows_with_prediction": int(
                np.isfinite(evaluation.random_forest.oob_predictions_).sum()
            )
            if evaluation.random_forest.oob_predictions_ is not None
            else 0,
            "oob_coverage": evaluation.random_forest.oob_coverage_,
            "oob_RMSE": evaluation.random_forest.oob_rmse_,
            "note": "Out-of-bag predictions aggregate only trees that did not train on each row; this is a training-period diagnostic, not the final chronological test score.",
        },
    )
    write_csv_rows(config.linear_coefficients_path, ["term", "coefficient"], coefficient_rows(evaluation.linear_artifacts))
    write_json(config.garch_path, evaluation.garch_params)
    primary_garch = evaluation.predictions["garch_1_1"].to_numpy(dtype=float)
    garch_conversion_rows: list[dict[str, Any]] = []
    for role, conversion, column, note in (
        (
            "primary",
            "E[s] via 80-point Gauss-Hermite quadrature",
            "garch_1_1",
            "Conditional mean of the standard-deviation target; aligned with squared-error point forecasting.",
        ),
        (
            "sensitivity",
            "sqrt(E[s^2]) analytic conversion",
            "garch_sqrt_expected_variance",
            "Square root of expected sample variance; retained to quantify the Jensen-gap sensitivity.",
        ),
    ):
        forecast = evaluation.predictions[column].to_numpy(dtype=float)
        metrics = regression_metrics(prepared.y_test, forecast)
        garch_conversion_rows.append(
            {
                "role": role,
                "conversion": conversion,
                "MAE": f"{metrics['MAE']:.8f}",
                "MSE": f"{metrics['MSE']:.8f}",
                "RMSE": f"{metrics['RMSE']:.8f}",
                "mean_forecast": f"{float(np.mean(forecast)):.8f}",
                "mean_difference_vs_primary": f"{float(np.mean(forecast - primary_garch)):.8f}",
                "maximum_difference_vs_primary": f"{float(np.max(np.abs(forecast - primary_garch))):.8f}",
                "method_note": note,
            }
        )
    write_csv_rows(
        config.garch_conversion_sensitivity_path,
        [
            "role", "conversion", "MAE", "MSE", "RMSE", "mean_forecast",
            "mean_difference_vs_primary", "maximum_difference_vs_primary", "method_note",
        ],
        garch_conversion_rows,
    )
    write_json(config.lstm_summary_path, evaluation.lstm_artifacts.metadata)
    export_lstm_history(config.lstm_history_path, evaluation.lstm_artifacts.history_rows)

    computational_rows = build_computational_rows(
        evaluation.timings,
        evaluation.complexities,
        len(prepared.train),
        len(prepared.test),
    )
    multidimensional_rows = build_multidimensional_rows(
        evaluation.ranked_rows,
        evaluation.timings,
        evaluation.complexities,
    )
    write_csv_rows(
        config.computational_profile_path,
        [
            "model", "fit_seconds", "predict_seconds", "total_seconds", "complexity_measure",
            "complexity_value", "train_rows", "test_rows", "timing_note",
        ],
        computational_rows,
    )
    write_csv_rows(
        config.multidimensional_comparison_path,
        [
            "accuracy_rank_by_RMSE", "model", "category", "MAE", "RMSE", "interpretability_level",
            "explanation_evidence", "main_interpretability_limit", "fit_seconds", "predict_seconds",
            "complexity", "reproducibility_assessment", "risk_management_assessment",
        ],
        multidimensional_rows,
    )
    write_csv_rows(
        config.robustness_path,
        [
            "volatility_window_days", "rank_by_RMSE", "model", "MAE", "MSE", "RMSE",
            "RMSE_vs_rolling_percent", "train_period", "test_period",
        ],
        robustness_rows,
    )
    test_segment_rows = build_test_segment_rows(evaluation.predictions)
    write_csv_rows(
        config.test_segment_path,
        [
            "test_segment", "start_date", "end_date", "observations", "rank_by_RMSE",
            "model", "MAE", "RMSE",
        ],
        test_segment_rows,
    )
    uncertainty_rows = build_block_bootstrap_rows(
        evaluation.predictions,
        random_seed=config.random_seed,
    )
    write_csv_rows(
        config.uncertainty_path,
        [
            "model", "RMSE", "rolling_RMSE", "RMSE_difference_vs_rolling",
            "bootstrap_median_difference", "bootstrap_95pct_lower", "bootstrap_95pct_upper",
            "bootstrap_share_better_than_rolling", "bootstrap_samples", "block_length_days",
            "method_note",
        ],
        uncertainty_rows,
    )
    regime_rows = build_regime_performance_rows(evaluation.predictions)
    write_csv_rows(
        config.regime_performance_path,
        [
            "volatility_regime", "observations", "actual_min", "actual_max",
            "lower_tercile_threshold", "upper_tercile_threshold", "rank_by_RMSE",
            "model", "MAE", "RMSE", "mean_prediction_bias",
        ],
        regime_rows,
    )
    walk_forward.predictions.to_csv(
        config.walk_forward_predictions_path,
        index=False,
        lineterminator="\n",
        date_format="%Y-%m-%d",
    )
    write_csv_rows(
        config.walk_forward_performance_path,
        ["rank_by_RMSE", "model", "category", "MAE", "MSE", "RMSE"],
        [
            row.as_csv_row(rank)
            for rank, row in enumerate(walk_forward.overall_rows, start=1)
        ],
    )
    write_csv_rows(
        config.walk_forward_fold_path,
        [
            "walk_forward_fold", "train_rows", "train_start", "train_end",
            "test_start", "test_end", "target_start", "target_end", "test_rows",
            "rank_by_RMSE", "model", "MAE", "MSE", "RMSE",
        ],
        walk_forward.fold_rows,
    )
    write_csv_rows(
        config.lstm_seed_stability_path,
        [
            "seed", "status", "best_epoch", "best_validation_mse_on_scaled_target",
            "fit_seconds", "predict_seconds", "MAE", "MSE", "RMSE",
        ],
        lstm_seed_rows,
    )

    write_json(
        config.run_metadata_path,
        build_run_metadata(
            config,
            prepared.raw_dataset,
            prepared.frame,
            prepared.train,
            prepared.test,
            evaluation.garch_params,
            evaluation.lstm_artifacts.metadata,
            evaluation.timings,
            evaluation.complexities,
            resolved_rf_max_features=evaluation.random_forest.resolved_max_features_,
        ),
    )
    draw_forecast_chart(evaluation.predictions, config.chart_path, config.rv_window)
    write_text(
        config.summary_path,
        build_model_summary_markdown(
            config,
            prepared.frame,
            prepared.train,
            prepared.test,
            evaluation.ranked_rows,
            evaluation.lstm_artifacts.metadata,
            computational_rows,
            robustness_rows,
            test_segment_rows,
            uncertainty_rows,
            regime_rows,
            walk_forward.overall_rows,
            lstm_seed_rows,
        ),
    )
    return [
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
    ]


def run_model_pipeline(config: ModelRunConfig) -> list[Path]:
    ensure_directory(config.output_dir)
    prepared = prepare_modelling_data(config)
    evaluation = evaluate_models(prepared, config)
    robustness_rows = run_robustness_checks(config, prepared, evaluation)
    walk_forward = run_walk_forward_checks(config, prepared, evaluation)
    lstm_seed_rows = build_lstm_seed_stability_rows(prepared, evaluation, config)
    return export_model_outputs(
        config,
        prepared,
        evaluation,
        robustness_rows,
        walk_forward,
        lstm_seed_rows,
    )


def run_model_command(args: argparse.Namespace) -> int:
    written_paths = run_model_pipeline(config_from_args(args))
    for path in written_paths:
        print(f"Wrote {path}")
    return 0


def main() -> int:
    parser = build_arg_parser()
    return run_model_command(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
