"""Configuration objects and constants for the EPQ pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


API_URL = "https://api.hyperliquid.xyz/info"
DEFAULT_COIN = "BTC"
DEFAULT_INTERVAL = "1d"
DEFAULT_START_DATE = "2023-02-26"
DEFAULT_WINDOW = 30
DEFAULT_USER_ADDRESS = "0x28e81E9fAC95AC1fae40870E4C08E6b94FcB1C23"
DEFAULT_TIMEOUT_SECONDS = 30

FEATURE_COLS = (
    "realised_volatility_30d",
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
)

LSTM_FEATURE_COLS = (
    "realised_volatility_30d",
    "log_return",
    "abs_return",
    "log_volume",
    "log_trade_count",
    "rolling_abs_return_7d",
    "rolling_return_std_7d",
    "rolling_abs_return_30d",
    "rolling_return_std_30d",
)


@dataclass(frozen=True)
class FetchConfig:
    coin: str = DEFAULT_COIN
    interval: str = DEFAULT_INTERVAL
    start_date: str = DEFAULT_START_DATE
    end_date: str = field(default_factory=lambda: datetime.now(UTC).date().isoformat())
    window: int = DEFAULT_WINDOW
    user_address: str | None = DEFAULT_USER_ADDRESS
    raw_output: Path = Path("data/raw/hyperliquid_BTC_1d_candles.csv")
    processed_output: Path = Path("data/processed/hyperliquid_BTC_1d_volatility.csv")
    metadata_output: Path = Path("data/raw/hyperliquid_BTC_1d_metadata.json")
    api_url: str = API_URL
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS


@dataclass(frozen=True)
class RandomForestConfig:
    n_estimators: int = 160
    max_depth: int = 7
    min_samples_leaf: int = 10
    max_features: int | None = None


@dataclass(frozen=True)
class LSTMConfig:
    sequence_length: int = 30
    hidden_size: int = 32
    batch_size: int = 32
    learning_rate: float = 0.003
    weight_decay: float = 1e-5
    max_epochs: int = 240
    early_stopping_patience: int = 30
    validation_fraction: float = 0.15


@dataclass(frozen=True)
class ModelRunConfig:
    input_path: Path = Path("data/processed/hyperliquid_BTC_1d_volatility.csv")
    output_dir: Path = Path("code/outputs")
    rv_window: int = DEFAULT_WINDOW
    robustness_windows: tuple[int, ...] = (14, 30)
    train_fraction: float = 0.8
    random_seed: int = 42
    random_forest: RandomForestConfig = field(default_factory=RandomForestConfig)
    lstm: LSTMConfig = field(default_factory=LSTMConfig)

    @property
    def rv_col(self) -> str:
        return f"realised_volatility_{self.rv_window}d"

    @property
    def target_col(self) -> str:
        return f"target_next_day_realised_volatility_{self.rv_window}d"

    @property
    def feature_cols(self) -> tuple[str, ...]:
        return tuple(self.rv_col if column == "realised_volatility_30d" else column for column in FEATURE_COLS)

    @property
    def lstm_feature_cols(self) -> tuple[str, ...]:
        return tuple(self.rv_col if column == "realised_volatility_30d" else column for column in LSTM_FEATURE_COLS)

    @property
    def performance_path(self) -> Path:
        return self.output_dir / "model_performance.csv"

    @property
    def predictions_path(self) -> Path:
        return self.output_dir / "model_predictions.csv"

    @property
    def feature_importance_path(self) -> Path:
        return self.output_dir / "random_forest_feature_importance.csv"

    @property
    def garch_path(self) -> Path:
        return self.output_dir / "garch_parameters.json"

    @property
    def linear_coefficients_path(self) -> Path:
        return self.output_dir / "linear_regression_coefficients.csv"

    @property
    def lstm_summary_path(self) -> Path:
        return self.output_dir / "lstm_training_summary.json"

    @property
    def lstm_history_path(self) -> Path:
        return self.output_dir / "lstm_training_history.csv"

    @property
    def run_metadata_path(self) -> Path:
        return self.output_dir / "model_run_metadata.json"

    @property
    def computational_profile_path(self) -> Path:
        return self.output_dir / "model_computational_profile.csv"

    @property
    def multidimensional_comparison_path(self) -> Path:
        return self.output_dir / "model_multidimensional_comparison.csv"

    @property
    def robustness_path(self) -> Path:
        return self.output_dir / "model_robustness_by_window.csv"

    @property
    def chart_path(self) -> Path:
        return self.output_dir / "volatility_forecast_comparison.png"

    @property
    def summary_path(self) -> Path:
        return self.output_dir / "model_summary.md"
