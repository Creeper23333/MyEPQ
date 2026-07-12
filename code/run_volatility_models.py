#!/usr/bin/env python3
"""Run first-pass Bitcoin volatility forecasting models.

This script produces reproducible output tables for the EPQ report.
"""

from __future__ import annotations

import csv
import copy
import json
import math
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

try:
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset
except ImportError:  # pragma: no cover - handled at runtime when torch is unavailable
    torch = None
    nn = None
    DataLoader = None
    TensorDataset = None


INPUT_PATH = Path("data/processed/hyperliquid_BTC_1d_volatility.csv")
OUTPUT_DIR = Path("code/outputs")
TARGET_COL = "target_next_day_realised_volatility_30d"
RV_COL = "realised_volatility_30d"
RANDOM_SEED = 42
LSTM_SEQUENCE_LENGTH = 30
LSTM_HIDDEN_SIZE = 32
LSTM_BATCH_SIZE = 32
LSTM_LEARNING_RATE = 0.003
LSTM_WEIGHT_DECAY = 1e-5
LSTM_MAX_EPOCHS = 240
LSTM_PATIENCE = 30
LSTM_VALIDATION_FRACTION = 0.15


def ensure_outputs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    numeric_cols = ["close", "log_return", RV_COL, "volume", "trade_count"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values("date").reset_index(drop=True)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["abs_return"] = out["log_return"].abs()
    out["log_volume"] = np.log1p(out["volume"])
    out["log_trade_count"] = np.log1p(out["trade_count"])

    for lag in [1, 2, 3, 7, 14]:
        out[f"return_lag_{lag}"] = out["log_return"].shift(lag)
        out[f"abs_return_lag_{lag}"] = out["abs_return"].shift(lag)
        out[f"rv_lag_{lag}"] = out[RV_COL].shift(lag)

    for window in [7, 14, 30]:
        out[f"rolling_abs_return_{window}d"] = out["abs_return"].rolling(window).mean()
        out[f"rolling_return_std_{window}d"] = out["log_return"].rolling(window).std()

    out[TARGET_COL] = out[RV_COL].shift(-1)
    return out


FEATURE_COLS = [
    RV_COL,
    "log_return",
    "abs_return",
    "log_volume",
    "log_trade_count",
    "return_lag_1",
    "return_lag_2",
    "return_lag_3",
    "return_lag_7",
    "return_lag_14",
    "abs_return_lag_1",
    "abs_return_lag_2",
    "abs_return_lag_3",
    "abs_return_lag_7",
    "abs_return_lag_14",
    "rv_lag_1",
    "rv_lag_2",
    "rv_lag_3",
    "rv_lag_7",
    "rv_lag_14",
    "rolling_abs_return_7d",
    "rolling_abs_return_14d",
    "rolling_abs_return_30d",
    "rolling_return_std_7d",
    "rolling_return_std_14d",
    "rolling_return_std_30d",
]

LSTM_FEATURE_COLS = [
    RV_COL,
    "log_return",
    "abs_return",
    "log_volume",
    "log_trade_count",
    "rolling_abs_return_7d",
    "rolling_return_std_7d",
    "rolling_abs_return_30d",
    "rolling_return_std_30d",
]


def modelling_frame(df: pd.DataFrame) -> pd.DataFrame:
    needed = ["date", TARGET_COL, *FEATURE_COLS]
    frame = df[needed].dropna().reset_index(drop=True)
    return frame


def split_frame(frame: pd.DataFrame, train_fraction: float = 0.8) -> tuple[pd.DataFrame, pd.DataFrame]:
    split_index = int(len(frame) * train_fraction)
    return frame.iloc[:split_index].copy(), frame.iloc[split_index:].copy()


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    error = y_true - y_pred
    mae = float(np.mean(np.abs(error)))
    mse = float(np.mean(error**2))
    rmse = float(math.sqrt(mse))
    return {"MAE": mae, "MSE": mse, "RMSE": rmse}


def build_lstm_sequences(
    features: np.ndarray,
    targets: np.ndarray,
    dates: np.ndarray,
    split_index: int,
    sequence_length: int = LSTM_SEQUENCE_LENGTH,
) -> dict[str, np.ndarray]:
    sequences: list[np.ndarray] = []
    seq_targets: list[float] = []
    seq_dates: list[Any] = []
    target_indices: list[int] = []

    for index in range(sequence_length - 1, len(features)):
        sequences.append(features[index - sequence_length + 1 : index + 1])
        seq_targets.append(float(targets[index]))
        seq_dates.append(dates[index])
        target_indices.append(index)

    x_seq = np.asarray(sequences, dtype=np.float32)
    y_seq = np.asarray(seq_targets, dtype=np.float32)
    date_seq = np.asarray(seq_dates)
    index_seq = np.asarray(target_indices, dtype=int)
    train_mask = index_seq < split_index
    test_mask = ~train_mask

    return {
        "x_train": x_seq[train_mask],
        "y_train": y_seq[train_mask],
        "dates_train": date_seq[train_mask],
        "x_test": x_seq[test_mask],
        "y_test": y_seq[test_mask],
        "dates_test": date_seq[test_mask],
    }


def torch_is_available() -> bool:
    return all(value is not None for value in [torch, nn, DataLoader, TensorDataset])


def set_torch_seed(seed: int = RANDOM_SEED) -> None:
    if not torch_is_available():
        return
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


_LSTMBase = nn.Module if nn is not None else object


def iso_date(value: Any) -> str:
    return str(pd.Timestamp(value).date())


class LSTMRegressor(_LSTMBase):
    def __init__(self, input_size: int, hidden_size: int = LSTM_HIDDEN_SIZE) -> None:
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        outputs, _ = self.lstm(x)
        return self.head(outputs[:, -1, :]).squeeze(-1)


def fit_lstm_model(
    x_train: np.ndarray,
    y_train: np.ndarray,
    sequence_length: int = LSTM_SEQUENCE_LENGTH,
) -> tuple[LSTMRegressor | None, dict[str, Any] | None]:
    if not torch_is_available():
        return None, None

    validation_count = max(1, int(len(x_train) * LSTM_VALIDATION_FRACTION))
    if len(x_train) <= validation_count + 8:
        validation_count = max(1, min(len(x_train) // 5, len(x_train) - 8))
    train_cut = len(x_train) - validation_count
    if train_cut <= 0:
        raise ValueError("Not enough sequence rows to fit the LSTM model")

    x_train_main = x_train[:train_cut]
    y_train_main = y_train[:train_cut]
    x_val = x_train[train_cut:]
    y_val = y_train[train_cut:]

    y_mean = float(y_train_main.mean())
    y_std = float(y_train_main.std())
    if y_std == 0.0:
        y_std = 1.0

    set_torch_seed(RANDOM_SEED)
    model = LSTMRegressor(input_size=x_train.shape[2])
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LSTM_LEARNING_RATE,
        weight_decay=LSTM_WEIGHT_DECAY,
    )
    loss_fn = nn.MSELoss()

    train_dataset = TensorDataset(
        torch.tensor(x_train_main, dtype=torch.float32),
        torch.tensor((y_train_main - y_mean) / y_std, dtype=torch.float32),
    )
    train_loader = DataLoader(train_dataset, batch_size=LSTM_BATCH_SIZE, shuffle=True)
    x_val_tensor = torch.tensor(x_val, dtype=torch.float32)
    y_val_tensor = torch.tensor((y_val - y_mean) / y_std, dtype=torch.float32)

    best_state: dict[str, torch.Tensor] | None = None
    best_val_loss = float("inf")
    best_epoch = 0
    patience_left = LSTM_PATIENCE

    for epoch in range(1, LSTM_MAX_EPOCHS + 1):
        model.train()
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = loss_fn(predictions, batch_y)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_predictions = model(x_val_tensor)
            val_loss = float(loss_fn(val_predictions, y_val_tensor).item())

        if val_loss + 1e-10 < best_val_loss:
            best_val_loss = val_loss
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
            patience_left = LSTM_PATIENCE
        else:
            patience_left -= 1
            if patience_left == 0:
                break

    if best_state is not None:
        model.load_state_dict(best_state)

    metadata = {
        "sequence_length": sequence_length,
        "sequence_features": LSTM_FEATURE_COLS,
        "hidden_size": LSTM_HIDDEN_SIZE,
        "batch_size": LSTM_BATCH_SIZE,
        "learning_rate": LSTM_LEARNING_RATE,
        "weight_decay": LSTM_WEIGHT_DECAY,
        "max_epochs": LSTM_MAX_EPOCHS,
        "early_stopping_patience": LSTM_PATIENCE,
        "epochs_trained": best_epoch,
        "best_validation_mse_on_scaled_target": best_val_loss,
        "train_sequences": int(len(x_train_main)),
        "validation_sequences": int(len(x_val)),
        "target_mean": y_mean,
        "target_std": y_std,
    }
    return model, metadata


def predict_lstm_model(
    model: LSTMRegressor,
    x_values: np.ndarray,
    target_mean: float,
    target_std: float,
) -> np.ndarray:
    model.eval()
    with torch.no_grad():
        predictions = model(torch.tensor(x_values, dtype=torch.float32)).cpu().numpy()
    return np.clip(predictions * target_std + target_mean, 0.0, None)


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


@dataclass
class TreeNode:
    prediction: float
    feature_index: int | None = None
    threshold: float | None = None
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class SimpleRandomForestRegressor:
    def __init__(
        self,
        n_estimators: int = 140,
        max_depth: int = 6,
        min_samples_leaf: int = 12,
        max_features: int | None = None,
        random_state: int = RANDOM_SEED,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.trees: list[TreeNode] = []
        self.feature_importances_: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleRandomForestRegressor":
        rng = np.random.default_rng(self.random_state)
        n_samples, n_features = x.shape
        max_features = self.max_features or max(1, int(math.sqrt(n_features)))
        importances = np.zeros(n_features, dtype=float)
        self.trees = []
        for _ in range(self.n_estimators):
            sample_idx = rng.integers(0, n_samples, size=n_samples)
            tree = self._build_tree(x[sample_idx], y[sample_idx], 0, rng, max_features, importances)
            self.trees.append(tree)
        total = float(importances.sum())
        self.feature_importances_ = importances / total if total > 0 else importances
        return self

    def _build_tree(
        self,
        x: np.ndarray,
        y: np.ndarray,
        depth: int,
        rng: np.random.Generator,
        max_features: int,
        importances: np.ndarray,
    ) -> TreeNode:
        prediction = float(np.mean(y))
        if depth >= self.max_depth or len(y) < 2 * self.min_samples_leaf or float(np.var(y)) < 1e-12:
            return TreeNode(prediction=prediction)

        n_features = x.shape[1]
        feature_indices = rng.choice(n_features, size=max_features, replace=False)
        parent_sse = float(np.sum((y - prediction) ** 2))
        best: dict[str, Any] | None = None

        for feature_index in feature_indices:
            values = x[:, feature_index]
            thresholds = np.unique(np.quantile(values, np.linspace(0.10, 0.90, 9)))
            for threshold in thresholds:
                left_mask = values <= threshold
                left_count = int(left_mask.sum())
                right_count = len(y) - left_count
                if left_count < self.min_samples_leaf or right_count < self.min_samples_leaf:
                    continue
                left_y = y[left_mask]
                right_y = y[~left_mask]
                left_sse = float(np.sum((left_y - np.mean(left_y)) ** 2))
                right_sse = float(np.sum((right_y - np.mean(right_y)) ** 2))
                gain = parent_sse - left_sse - right_sse
                if gain > 1e-14 and (best is None or gain > best["gain"]):
                    best = {
                        "feature_index": int(feature_index),
                        "threshold": float(threshold),
                        "left_mask": left_mask,
                        "gain": gain,
                    }

        if best is None:
            return TreeNode(prediction=prediction)

        importances[best["feature_index"]] += best["gain"]
        left_mask = best["left_mask"]
        return TreeNode(
            prediction=prediction,
            feature_index=best["feature_index"],
            threshold=best["threshold"],
            left=self._build_tree(x[left_mask], y[left_mask], depth + 1, rng, max_features, importances),
            right=self._build_tree(x[~left_mask], y[~left_mask], depth + 1, rng, max_features, importances),
        )

    def predict(self, x: np.ndarray) -> np.ndarray:
        if not self.trees:
            raise ValueError("Model has not been fitted")
        predictions = np.column_stack([self._predict_tree(tree, x) for tree in self.trees])
        return predictions.mean(axis=1)

    def _predict_tree(self, tree: TreeNode, x: np.ndarray) -> np.ndarray:
        return np.array([self._predict_one(tree, row) for row in x], dtype=float)

    def _predict_one(self, node: TreeNode, row: np.ndarray) -> float:
        while node.feature_index is not None and node.threshold is not None:
            if row[node.feature_index] <= node.threshold:
                node = node.left or node
            else:
                node = node.right or node
        return node.prediction


def fit_linear_regression(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    x_design = np.column_stack([np.ones(len(x)), x])
    ridge = np.eye(x_design.shape[1]) * 1e-8
    ridge[0, 0] = 0.0
    return np.linalg.solve(x_design.T @ x_design + ridge, x_design.T @ y)


def predict_linear_regression(x: np.ndarray, beta: np.ndarray) -> np.ndarray:
    x_design = np.column_stack([np.ones(len(x)), x])
    return x_design @ beta


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def format_metric(value: float) -> str:
    return f"{value:.8f}"


def draw_chart(predictions: pd.DataFrame, output_path: Path) -> None:
    plot_df = predictions.tail(min(180, len(predictions))).reset_index(drop=True)
    series = {
        "Actual": (plot_df["actual"].to_numpy(dtype=float), (28, 28, 28)),
        "Rolling": (plot_df["rolling_historical"].to_numpy(dtype=float), (75, 120, 184)),
        "GARCH": (plot_df["garch_1_1"].to_numpy(dtype=float), (210, 102, 45)),
        "Lagged Linear": (plot_df["lagged_linear_regression"].to_numpy(dtype=float), (115, 88, 188)),
        "Random Forest": (plot_df["random_forest"].to_numpy(dtype=float), (44, 145, 95)),
    }
    if "lstm" in plot_df:
        series["LSTM"] = (plot_df["lstm"].to_numpy(dtype=float), (185, 65, 65))
    all_values = np.concatenate([values for values, _ in series.values()])
    min_y = float(np.nanmin(all_values)) * 0.92
    max_y = float(np.nanmax(all_values)) * 1.08
    if max_y <= min_y:
        max_y = min_y + 0.01

    width, height = 1200, 720
    margin_left, margin_right = 90, 40
    margin_top, margin_bottom = 90, 95
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((margin_left, 28), "Hyperliquid BTC 30-day Realised Volatility Forecasts", fill=(20, 20, 20), font=font)
    draw.text((margin_left, 52), "Out-of-sample test window, last 180 observations shown", fill=(80, 80, 80), font=font)

    # Axes and grid
    axis_color = (130, 130, 130)
    grid_color = (225, 225, 225)
    draw.line((margin_left, margin_top, margin_left, margin_top + plot_height), fill=axis_color)
    draw.line((margin_left, margin_top + plot_height, margin_left + plot_width, margin_top + plot_height), fill=axis_color)

    for i in range(6):
        y_value = min_y + (max_y - min_y) * i / 5
        y = margin_top + plot_height - int((y_value - min_y) / (max_y - min_y) * plot_height)
        draw.line((margin_left, y, margin_left + plot_width, y), fill=grid_color)
        draw.text((15, y - 6), f"{y_value:.3f}", fill=(80, 80, 80), font=font)

    def point(index: int, value: float) -> tuple[int, int]:
        x = margin_left + int(index / max(1, len(plot_df) - 1) * plot_width)
        y = margin_top + plot_height - int((value - min_y) / (max_y - min_y) * plot_height)
        return x, y

    for label, (values, color) in series.items():
        points = [point(i, float(value)) for i, value in enumerate(values) if np.isfinite(value)]
        if len(points) > 1:
            draw.line(points, fill=color, width=3 if label == "Actual" else 2)

    legend_x = margin_left
    legend_y = height - 65
    for label, (_, color) in series.items():
        draw.line((legend_x, legend_y + 8, legend_x + 35, legend_y + 8), fill=color, width=4)
        draw.text((legend_x + 44, legend_y), label, fill=(30, 30, 30), font=font)
        legend_x += 170

    first_date = plot_df["date"].iloc[0]
    last_date = plot_df["date"].iloc[-1]
    draw.text((margin_left, height - 35), str(first_date.date()), fill=(80, 80, 80), font=font)
    draw.text((margin_left + plot_width - 80, height - 35), str(last_date.date()), fill=(80, 80, 80), font=font)
    image.save(output_path)


def main() -> int:
    ensure_outputs()
    df = load_dataset(INPUT_PATH)
    featured = add_features(df)
    frame = modelling_frame(featured)
    train, test = split_frame(frame)

    x_train = train[FEATURE_COLS].to_numpy(dtype=float)
    y_train = train[TARGET_COL].to_numpy(dtype=float)
    x_test = test[FEATURE_COLS].to_numpy(dtype=float)
    y_test = test[TARGET_COL].to_numpy(dtype=float)

    # Standardization helps linear regression; the tree model receives the same scaled input for consistency.
    x_mean = x_train.mean(axis=0)
    x_std = x_train.std(axis=0)
    x_std[x_std == 0] = 1.0
    x_train_scaled = (x_train - x_mean) / x_std
    x_test_scaled = (x_test - x_mean) / x_std

    rolling_pred = test[RV_COL].to_numpy(dtype=float)

    garch_train_returns = df[df["date"] <= train["date"].iloc[-1]]["log_return"].dropna().to_numpy(dtype=float)
    garch_params = fit_garch_grid(garch_train_returns)
    featured["garch_1_1"] = garch_realised_vol_forecast(featured, garch_params)
    garch_pred = featured.loc[test.index, "garch_1_1"].to_numpy(dtype=float)

    linear_beta = fit_linear_regression(x_train_scaled, y_train)
    linear_pred = np.clip(predict_linear_regression(x_test_scaled, linear_beta), 0.0, None)

    rf = SimpleRandomForestRegressor().fit(x_train_scaled, y_train)
    rf_pred = np.clip(rf.predict(x_test_scaled), 0.0, None)

    lstm_metadata: dict[str, Any] | None = None
    lstm_pred: np.ndarray | None = None
    if torch_is_available():
        lstm_train_features = train[LSTM_FEATURE_COLS].to_numpy(dtype=float)
        lstm_mean = lstm_train_features.mean(axis=0)
        lstm_std = lstm_train_features.std(axis=0)
        lstm_std[lstm_std == 0] = 1.0
        full_lstm_features = frame[LSTM_FEATURE_COLS].to_numpy(dtype=float)
        full_lstm_scaled = (full_lstm_features - lstm_mean) / lstm_std
        lstm_sequences = build_lstm_sequences(
            full_lstm_scaled,
            frame[TARGET_COL].to_numpy(dtype=float),
            frame["date"].to_numpy(),
            split_index=len(train),
            sequence_length=LSTM_SEQUENCE_LENGTH,
        )
        lstm_model, lstm_metadata = fit_lstm_model(
            lstm_sequences["x_train"],
            lstm_sequences["y_train"],
            sequence_length=LSTM_SEQUENCE_LENGTH,
        )
        if lstm_model is not None and lstm_metadata is not None:
            lstm_metadata["train_sequence_start_date"] = iso_date(lstm_sequences["dates_train"][0])
            lstm_metadata["train_sequence_end_date"] = iso_date(lstm_sequences["dates_train"][-1])
            lstm_metadata["test_sequence_start_date"] = iso_date(lstm_sequences["dates_test"][0])
            lstm_metadata["test_sequence_end_date"] = iso_date(lstm_sequences["dates_test"][-1])
            lstm_pred = predict_lstm_model(
                lstm_model,
                lstm_sequences["x_test"],
                target_mean=float(lstm_metadata["target_mean"]),
                target_std=float(lstm_metadata["target_std"]),
            )

    model_predictions = pd.DataFrame(
        {
            "date": test["date"].to_numpy(),
            "actual": y_test,
            "rolling_historical": rolling_pred,
            "garch_1_1": garch_pred,
            "lagged_linear_regression": linear_pred,
            "random_forest": rf_pred,
        }
    )
    if lstm_pred is not None:
        model_predictions["lstm"] = lstm_pred

    model_rows: list[dict[str, Any]] = []
    model_specs = [
        ("Rolling historical volatility", "rolling_historical", "Benchmark"),
        ("GARCH(1,1)", "garch_1_1", "Traditional statistical"),
        ("Lagged linear regression", "lagged_linear_regression", "Interpretable lag-feature model"),
        ("Random Forest", "random_forest", "Machine learning"),
    ]
    if lstm_pred is not None:
        model_specs.append(("LSTM", "lstm", "Machine learning"))
    for name, col, category in model_specs:
        scores = metrics(y_test, model_predictions[col].to_numpy(dtype=float))
        model_rows.append(
            {
                "model": name,
                "category": category,
                "MAE": format_metric(scores["MAE"]),
                "MSE": format_metric(scores["MSE"]),
                "RMSE": format_metric(scores["RMSE"]),
            }
        )
    model_rows.sort(key=lambda row: float(row["RMSE"]))
    for rank, row in enumerate(model_rows, start=1):
        row["rank_by_RMSE"] = rank

    predictions_path = OUTPUT_DIR / "model_predictions.csv"
    model_predictions.to_csv(predictions_path, index=False, lineterminator="\n")

    performance_path = OUTPUT_DIR / "model_performance.csv"
    write_csv(
        performance_path,
        model_rows,
        ["rank_by_RMSE", "model", "category", "MAE", "MSE", "RMSE"],
    )

    feature_importance_path = OUTPUT_DIR / "random_forest_feature_importance.csv"
    importances = rf.feature_importances_ if rf.feature_importances_ is not None else np.zeros(len(FEATURE_COLS))
    importance_rows = [
        {"feature": feature, "importance": f"{importance:.8f}"}
        for feature, importance in sorted(zip(FEATURE_COLS, importances), key=lambda item: item[1], reverse=True)
    ]
    write_csv(feature_importance_path, importance_rows, ["feature", "importance"])

    garch_path = OUTPUT_DIR / "garch_parameters.json"
    garch_path.write_text(json.dumps(garch_params, indent=2) + "\n", encoding="utf-8")

    lstm_path = OUTPUT_DIR / "lstm_training_summary.json"
    if lstm_metadata is not None:
        lstm_metadata["torch_version"] = torch.__version__ if torch is not None else None
        lstm_metadata["test_sequences"] = int(len(model_predictions))
    else:
        lstm_metadata = {
            "status": "skipped",
            "reason": "PyTorch is not available in the current Python environment.",
        }
    lstm_path.write_text(json.dumps(lstm_metadata, indent=2) + "\n", encoding="utf-8")

    chart_path = OUTPUT_DIR / "volatility_forecast_comparison.png"
    draw_chart(model_predictions, chart_path)

    summary_path = OUTPUT_DIR / "model_summary.md"
    best = model_rows[0]
    summary = f"""# Current Volatility Model Results

Generated: {datetime.now(UTC).replace(microsecond=0).isoformat()}

## Dataset

- Source file: `{INPUT_PATH}`
- Model frame rows: {len(frame)}
- Train rows: {len(train)} ({train['date'].iloc[0].date()} to {train['date'].iloc[-1].date()})
- Test rows: {len(test)} ({test['date'].iloc[0].date()} to {test['date'].iloc[-1].date()})
- Forecast target: next-day 30-day realised volatility, not annualised

## Result

Best current model by RMSE: **{best['model']}** with RMSE `{best['RMSE']}`.

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
"""
    for row in model_rows:
        summary += f"| {row['rank_by_RMSE']} | {row['model']} | {row['category']} | {row['MAE']} | {row['MSE']} | {row['RMSE']} |\n"

    summary += f"""
## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting, then converted into a 30-day realised-volatility forecast using the most recent 29 observed returns plus the one-step-ahead conditional variance.
- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.
"""
    if lstm_metadata is not None:
        summary += f"- LSTM is fitted using PyTorch on rolling {LSTM_SEQUENCE_LENGTH}-day sequences of core market features. Early stopping selected epoch {lstm_metadata['epochs_trained']} using a chronological validation split.\n"
    else:
        summary += "- LSTM was skipped because PyTorch is not available in the current Python environment.\n"

    summary += f"""

## Output Files

- `{performance_path}`
- `{predictions_path}`
- `{feature_importance_path}`
- `{garch_path}`
- `{lstm_path}`
- `{chart_path}`
"""
    summary_path.write_text(summary, encoding="utf-8")

    print(f"Wrote {performance_path}")
    print(f"Wrote {predictions_path}")
    print(f"Wrote {feature_importance_path}")
    print(f"Wrote {garch_path}")
    print(f"Wrote {lstm_path}")
    print(f"Wrote {chart_path}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
