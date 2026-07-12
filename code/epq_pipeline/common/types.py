"""Shared dataclasses for pipeline state and model outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class StandardizationStats:
    mean: np.ndarray
    std: np.ndarray


@dataclass(frozen=True)
class PerformanceRow:
    model: str
    category: str
    mae: float
    mse: float
    rmse: float

    def as_csv_row(self, rank: int) -> dict[str, Any]:
        return {
            "rank_by_RMSE": rank,
            "model": self.model,
            "category": self.category,
            "MAE": f"{self.mae:.8f}",
            "MSE": f"{self.mse:.8f}",
            "RMSE": f"{self.rmse:.8f}",
        }


@dataclass(frozen=True)
class ChronologicalSplit:
    frame: pd.DataFrame
    train: pd.DataFrame
    test: pd.DataFrame

