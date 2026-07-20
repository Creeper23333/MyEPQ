"""Feature engineering and dataset splitting."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from epq_pipeline.common.types import ChronologicalSplit, StandardizationStats


def validate_model_input_dataset(
    df: pd.DataFrame,
    rv_col: str,
    rv_window: int | None = None,
) -> None:
    """Reject corrupted processed inputs instead of silently dropping bad rows."""
    required = {"date", "close", "log_return", "volume", "trade_count"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Processed dataset is missing required columns: {missing}")
    if len(df) < 2:
        raise ValueError("Processed dataset needs at least two daily rows")
    if df["date"].isna().any():
        raise ValueError("Processed dataset contains invalid dates")
    if df["date"].duplicated().any():
        raise ValueError("Processed dataset contains duplicate dates")
    if not df["date"].is_monotonic_increasing:
        raise ValueError("Processed dataset dates must be strictly increasing")
    date_gaps = df["date"].diff().dropna()
    if not (date_gaps == pd.Timedelta(days=1)).all():
        raise ValueError("Processed dataset must contain one continuous row per UTC day")

    close = df["close"].to_numpy(dtype=float)
    volume = df["volume"].to_numpy(dtype=float)
    trade_count = df["trade_count"].to_numpy(dtype=float)
    if not np.all(np.isfinite(close)) or np.any(close <= 0.0):
        raise ValueError("Processed close prices must be finite and positive")
    if not np.all(np.isfinite(volume)) or np.any(volume < 0.0):
        raise ValueError("Processed volumes must be finite and non-negative")
    if not np.all(np.isfinite(trade_count)) or np.any(trade_count < 0.0):
        raise ValueError("Processed trade counts must be finite and non-negative")
    if not np.allclose(trade_count, np.round(trade_count)):
        raise ValueError("Processed trade counts must be whole numbers")

    observed_returns = df["log_return"].to_numpy(dtype=float)
    expected_returns = np.full(len(df), np.nan, dtype=float)
    expected_returns[1:] = np.log(close[1:] / close[:-1])
    if not np.allclose(observed_returns, expected_returns, rtol=1e-10, atol=1e-12, equal_nan=True):
        raise ValueError("Processed log returns do not match adjacent close prices")

    if rv_col in df.columns:
        observed_rv = df[rv_col].to_numpy(dtype=float)
        if np.any(np.isfinite(observed_rv) & (observed_rv < 0.0)):
            raise ValueError(f"{rv_col} contains negative volatility")
        if rv_window is not None:
            expected_rv = (
                pd.Series(expected_returns)
                .rolling(rv_window)
                .std(ddof=1)
                .to_numpy(dtype=float)
            )
            if not np.allclose(observed_rv, expected_rv, rtol=1e-9, atol=1e-12, equal_nan=True):
                raise ValueError(f"{rv_col} does not match volatility recomputed from log returns")


def load_dataset(
    path: str | bytes | "os.PathLike[str]" | "os.PathLike[bytes]",
    rv_col: str,
    rv_window: int | None = None,
) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"date", "close", "log_return", "volume", "trade_count"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Processed dataset is missing required columns: {missing}")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric_cols = ["close", "log_return", rv_col, "volume", "trade_count"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    validate_model_input_dataset(df, rv_col, rv_window)
    return df.reset_index(drop=True)


def ensure_realised_volatility(df: pd.DataFrame, rv_col: str, window: int) -> pd.DataFrame:
    if window < 2:
        raise ValueError("Realised-volatility window must be at least two observations")
    out = df.copy()
    if rv_col not in out.columns:
        out[rv_col] = out["log_return"].rolling(window).std(ddof=1)
    return out


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

    # A row dated t contains information observed through t and predicts the
    # rolling-volatility value after the next completed candle, dated t + 1.
    # Retaining both dates prevents forecast-origin and target dates from
    # being conflated in exported evidence.
    out["target_date"] = out["date"].shift(-1)
    out[target_col] = out[rv_col].shift(-1)
    return out


def build_modelling_frame(df: pd.DataFrame, feature_cols: tuple[str, ...], target_col: str) -> pd.DataFrame:
    needed = ["date", "target_date", target_col, *feature_cols]
    return df[needed].dropna().reset_index(drop=True)


def chronological_split(frame: pd.DataFrame, train_fraction: float) -> ChronologicalSplit:
    split_index = int(len(frame) * train_fraction)
    if split_index <= 0 or split_index >= len(frame):
        raise ValueError("Chronological split must leave at least one row in both train and test sets")
    train = frame.iloc[:split_index].copy()
    test = frame.iloc[split_index:].copy()
    return ChronologicalSplit(frame=frame, train=train, test=test)


def chronological_split_by_date(frame: pd.DataFrame, test_start_date: str) -> ChronologicalSplit:
    """Use a stable forecast-origin cutoff so appended data only extends the test set."""
    cutoff = pd.Timestamp(test_start_date)
    train = frame.loc[frame["date"] < cutoff].copy()
    test = frame.loc[frame["date"] >= cutoff].copy()
    if train.empty or test.empty:
        raise ValueError(
            "Fixed chronological cutoff must leave at least one row in both train and test sets"
        )
    if train["date"].max() >= test["date"].min():
        raise ValueError("Fixed chronological split contains overlapping dates")
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
