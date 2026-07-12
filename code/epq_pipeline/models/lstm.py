"""PyTorch LSTM regressor and training utilities."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

import numpy as np

from epq_pipeline.config import LSTMConfig

try:
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset
except ImportError:  # pragma: no cover
    torch = None
    nn = None
    DataLoader = None
    TensorDataset = None


def torch_is_available() -> bool:
    return all(value is not None for value in [torch, nn, DataLoader, TensorDataset])


def set_torch_seed(seed: int) -> None:
    if not torch_is_available():
        return
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


_LSTMBase = nn.Module if nn is not None else object


@dataclass
class LSTMTrainingArtifacts:
    model: Any
    metadata: dict[str, Any]
    history_rows: list[dict[str, Any]]


def skipped_lstm_artifacts(reason: str) -> LSTMTrainingArtifacts:
    return LSTMTrainingArtifacts(
        model=None,
        metadata={"status": "skipped", "reason": reason},
        history_rows=[],
    )


class LSTMRegressor(_LSTMBase):
    def __init__(self, input_size: int, hidden_size: int) -> None:
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
    config: LSTMConfig,
    random_seed: int,
) -> LSTMTrainingArtifacts:
    if not torch_is_available():
        return skipped_lstm_artifacts("PyTorch is not available in the current Python environment.")

    validation_count = max(1, int(len(x_train) * config.validation_fraction))
    if len(x_train) <= validation_count + 8:
        validation_count = max(1, min(len(x_train) // 5, len(x_train) - 8))
    train_cut = len(x_train) - validation_count
    if train_cut <= 0:
        return skipped_lstm_artifacts("Not enough sequence rows to train the LSTM.")

    x_train_main = x_train[:train_cut]
    y_train_main = y_train[:train_cut]
    x_val = x_train[train_cut:]
    y_val = y_train[train_cut:]

    y_mean = float(y_train_main.mean())
    y_std = float(y_train_main.std())
    if y_std == 0.0:
        y_std = 1.0

    set_torch_seed(random_seed)
    model = LSTMRegressor(input_size=x_train.shape[2], hidden_size=config.hidden_size)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )
    loss_fn = nn.MSELoss()

    train_dataset = TensorDataset(
        torch.tensor(x_train_main, dtype=torch.float32),
        torch.tensor((y_train_main - y_mean) / y_std, dtype=torch.float32),
    )
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
    x_val_tensor = torch.tensor(x_val, dtype=torch.float32)
    y_val_tensor = torch.tensor((y_val - y_mean) / y_std, dtype=torch.float32)

    best_state: dict[str, torch.Tensor] | None = None
    best_val_loss = float("inf")
    best_epoch = 0
    patience_left = config.early_stopping_patience
    history_rows: list[dict[str, Any]] = []

    for epoch in range(1, config.max_epochs + 1):
        model.train()
        batch_losses: list[float] = []
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = loss_fn(predictions, batch_y)
            loss.backward()
            optimizer.step()
            batch_losses.append(float(loss.item()))

        average_train_loss = float(np.mean(batch_losses)) if batch_losses else float("nan")
        model.eval()
        with torch.no_grad():
            val_predictions = model(x_val_tensor)
            val_loss = float(loss_fn(val_predictions, y_val_tensor).item())

        history_rows.append(
            {
                "epoch": epoch,
                "train_mse_on_scaled_target": average_train_loss,
                "validation_mse_on_scaled_target": val_loss,
            }
        )

        if val_loss + 1e-10 < best_val_loss:
            best_val_loss = val_loss
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
            patience_left = config.early_stopping_patience
        else:
            patience_left -= 1
            if patience_left == 0:
                break

    if best_state is not None:
        model.load_state_dict(best_state)

    metadata = {
        "status": "trained",
        "sequence_length": config.sequence_length,
        "hidden_size": config.hidden_size,
        "batch_size": config.batch_size,
        "learning_rate": config.learning_rate,
        "weight_decay": config.weight_decay,
        "max_epochs": config.max_epochs,
        "early_stopping_patience": config.early_stopping_patience,
        "validation_fraction": config.validation_fraction,
        "epochs_trained": best_epoch,
        "best_validation_mse_on_scaled_target": best_val_loss,
        "train_sequences": int(len(x_train_main)),
        "validation_sequences": int(len(x_val)),
        "target_mean": y_mean,
        "target_std": y_std,
        "torch_version": torch.__version__ if torch is not None else None,
    }
    return LSTMTrainingArtifacts(model=model, metadata=metadata, history_rows=history_rows)


def predict_lstm_model(
    artifacts: LSTMTrainingArtifacts,
    x_values: np.ndarray,
    target_mean: float,
    target_std: float,
) -> np.ndarray:
    if artifacts.model is None:
        raise ValueError("LSTM model is not available for prediction")
    artifacts.model.eval()
    with torch.no_grad():
        predictions = artifacts.model(torch.tensor(x_values, dtype=torch.float32)).cpu().numpy()
    return np.clip(predictions * target_std + target_mean, 0.0, None)
