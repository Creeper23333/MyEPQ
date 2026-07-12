"""Feature engineering and dataset splitting."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from epq_pipeline.common.types import ChronologicalSplit, StandardizationStats


def load_dataset(path: str | bytes | "os.PathLike[str]" | "os.PathLike[bytes]", rv_col: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    numeric_cols = ["close", "log_return", rv_col, "volume", "trade_count"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values("date").reset_index(drop=True)


def add_base_features(df: pd.DataFrame, rv_col: str, target_col: str) -> pd.DataFrame:
    out = df.copy()
    out["abs_return"] = out["log_return"].abs()
    out["log_volume"] = np.log1p(out["volume"])
    out["log_trade_count"] = np.log1p(out["trade_count"])

    for lag in [1, 2, 3, 7, 14]:
        out[f"return_lag_{lag}"] = out["log_return"].shift(lag)
        out[f"abs_return_lag_{lag}"] = out["abs_return"].shift(lag)
        out[f"rv_lag_{lag}"] = out[rv_col].shift(lag)

    for window in [7, 14, 30]:
        out[f"rolling_abs_return_{window}d"] = out["abs_return"].rolling(window).mean()
        out[f"rolling_return_std_{window}d"] = out["log_return"].rolling(window).std()

    out[target_col] = out[rv_col].shift(-1)
    return out


def build_modelling_frame(df: pd.DataFrame, feature_cols: tuple[str, ...], target_col: str) -> pd.DataFrame:
    needed = ["date", target_col, *feature_cols]
    return df[needed].dropna().reset_index(drop=True)


def chronological_split(frame: pd.DataFrame, train_fraction: float) -> ChronologicalSplit:
    split_index = int(len(frame) * train_fraction)
    if split_index <= 0 or split_index >= len(frame):
        raise ValueError("Chronological split must leave at least one row in both train and test sets")
    train = frame.iloc[:split_index].copy()
    test = frame.iloc[split_index:].copy()
    return ChronologicalSplit(frame=frame, train=train, test=test)


def fit_standardization_stats(values: np.ndarray) -> StandardizationStats:
    mean = values.mean(axis=0)
    std = values.std(axis=0)
    std[std == 0] = 1.0
    return StandardizationStats(mean=mean, std=std)


def apply_standardization(values: np.ndarray, stats: StandardizationStats) -> np.ndarray:
    return (values - stats.mean) / stats.std


def build_lstm_sequences(
    features: np.ndarray,
    targets: np.ndarray,
    dates: np.ndarray,
    split_index: int,
    sequence_length: int,
) -> dict[str, np.ndarray]:
    sequences: list[np.ndarray] = []
    seq_targets: list[float] = []
    seq_dates: list[Any] = []
    target_indices: list[int] = []
    feature_count = int(features.shape[1]) if features.ndim == 2 else 0

    for index in range(sequence_length - 1, len(features)):
        sequences.append(features[index - sequence_length + 1 : index + 1])
        seq_targets.append(float(targets[index]))
        seq_dates.append(dates[index])
        target_indices.append(index)

    if sequences:
        x_seq = np.asarray(sequences, dtype=np.float32)
    else:
        x_seq = np.empty((0, sequence_length, feature_count), dtype=np.float32)
    y_seq = np.asarray(seq_targets, dtype=np.float32) if seq_targets else np.empty((0,), dtype=np.float32)
    date_seq = np.asarray(seq_dates) if seq_dates else np.asarray([], dtype=object)
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
