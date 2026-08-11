"""Standard scikit-learn Random Forest with chronological validation tuning."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from epq_pipeline.config import RandomForestConfig
from epq_pipeline.models.metrics import regression_metrics

try:
    import sklearn
    from sklearn.ensemble import RandomForestRegressor
except ImportError:  # pragma: no cover - exercised only in an incomplete runtime
    sklearn = None
    RandomForestRegressor = None


def sklearn_is_available() -> bool:
    return sklearn is not None and RandomForestRegressor is not None


class StandardRandomForestRegressor:
    """Wrap sklearn's audited implementation and retain project diagnostics.

    Hyperparameters are selected on the final chronological part of the
    training period only. The selected configuration is then refitted on all
    pre-test rows with out-of-bag predictions enabled. The final test set is
    never used for model selection.
    """

    def __init__(self, config: RandomForestConfig, random_state: int) -> None:
        self.config = config
        self.random_state = random_state
        self.model: Any | None = None
        self.feature_importances_: np.ndarray | None = None
        self.oob_predictions_: np.ndarray | None = None
        self.oob_rmse_: float | None = None
        self.oob_coverage_: float = 0.0
        self.resolved_max_features_: int | None = None
        self.selected_params_: dict[str, Any] = {}
        self.tuning_rows_: list[dict[str, Any]] = []
        self.tuning_train_rows_: int = 0
        self.tuning_validation_rows_: int = 0

    def _new_model(
        self,
        *,
        max_depth: int | None,
        min_samples_leaf: int,
        max_features: int | float | str | None,
        oob_score: bool,
    ) -> Any:
        if not sklearn_is_available():
            raise ImportError(
                "scikit-learn is required for the standard Random Forest implementation"
            )
        return RandomForestRegressor(
            n_estimators=self.config.n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            bootstrap=True,
            oob_score=oob_score,
            random_state=self.random_state,
            n_jobs=1,
        )

    def _candidate_params(self) -> list[dict[str, Any]]:
        if self.config.tune_hyperparameters and self.config.tuning_candidates:
            return [
                {
                    "max_depth": max_depth,
                    "min_samples_leaf": min_samples_leaf,
                    "max_features": max_features,
                }
                for max_depth, min_samples_leaf, max_features in self.config.tuning_candidates
            ]
        return [
            {
                "max_depth": self.config.max_depth,
                "min_samples_leaf": self.config.min_samples_leaf,
                "max_features": self.config.max_features,
            }
        ]

    def fit(self, x: np.ndarray, y: np.ndarray) -> "StandardRandomForestRegressor":
        if x.ndim != 2 or y.ndim != 1 or len(x) != len(y) or len(y) == 0:
            raise ValueError(
                "Random Forest needs non-empty 2D features and aligned 1D targets"
            )
        if not 0.0 < self.config.validation_fraction < 0.5:
            raise ValueError("Random Forest validation_fraction must be between 0 and 0.5")

        n_samples, n_features = x.shape
        if isinstance(self.config.max_features, int) and not (
            1 <= self.config.max_features <= n_features
        ):
            raise ValueError(
                "Random Forest max_features must be between 1 and the feature count"
            )

        validation_rows = max(1, int(n_samples * self.config.validation_fraction))
        tuning_train_rows = n_samples - validation_rows
        if tuning_train_rows < 20:
            raise ValueError(
                "Random Forest chronological tuning needs at least 20 fitting rows"
            )
        self.tuning_train_rows_ = tuning_train_rows
        self.tuning_validation_rows_ = validation_rows

        tuning_rows: list[dict[str, Any]] = []
        candidates = self._candidate_params()
        for candidate_index, params in enumerate(candidates, start=1):
            max_features = params["max_features"]
            if isinstance(max_features, int) and not 1 <= max_features <= n_features:
                raise ValueError(
                    "Random Forest max_features must be between 1 and the feature count"
                )
            candidate = self._new_model(**params, oob_score=False)
            candidate.fit(x[:tuning_train_rows], y[:tuning_train_rows])
            validation_prediction = np.clip(
                candidate.predict(x[tuning_train_rows:]),
                0.0,
                None,
            )
            scores = regression_metrics(
                y[tuning_train_rows:],
                validation_prediction,
            )
            tuning_rows.append(
                {
                    "candidate": candidate_index,
                    "n_estimators": self.config.n_estimators,
                    "max_depth": params["max_depth"],
                    "min_samples_leaf": params["min_samples_leaf"],
                    "max_features": params["max_features"],
                    "tuning_train_rows": tuning_train_rows,
                    "validation_rows": validation_rows,
                    "validation_MAE": scores["MAE"],
                    "validation_RMSE": scores["RMSE"],
                    "validation_QLIKE": scores["QLIKE"],
                    "selected": False,
                }
            )

        selected = min(
            tuning_rows,
            key=lambda row: (
                float(row["validation_RMSE"]),
                float(row["validation_QLIKE"]),
                int(row["candidate"]),
            ),
        )
        selected["selected"] = True
        self.tuning_rows_ = tuning_rows
        self.selected_params_ = {
            "n_estimators": self.config.n_estimators,
            "max_depth": selected["max_depth"],
            "min_samples_leaf": selected["min_samples_leaf"],
            "max_features": selected["max_features"],
        }

        self.model = self._new_model(
            max_depth=selected["max_depth"],
            min_samples_leaf=int(selected["min_samples_leaf"]),
            max_features=selected["max_features"],
            oob_score=True,
        )
        self.model.fit(x, y)
        self.feature_importances_ = np.asarray(
            self.model.feature_importances_,
            dtype=float,
        )
        self.oob_predictions_ = np.asarray(
            self.model.oob_prediction_,
            dtype=float,
        )
        oob_mask = np.isfinite(self.oob_predictions_)
        self.oob_coverage_ = float(np.mean(oob_mask))
        self.oob_rmse_ = (
            float(
                np.sqrt(
                    np.mean(
                        (y[oob_mask] - self.oob_predictions_[oob_mask]) ** 2
                    )
                )
            )
            if np.any(oob_mask)
            else None
        )
        if self.model.estimators_:
            self.resolved_max_features_ = int(
                self.model.estimators_[0].max_features_
            )
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model has not been fitted")
        return np.clip(np.asarray(self.model.predict(x), dtype=float), 0.0, None)

    @property
    def node_count(self) -> int:
        if self.model is None:
            return 0
        return int(
            sum(estimator.tree_.node_count for estimator in self.model.estimators_)
        )

    @property
    def metadata(self) -> dict[str, Any]:
        return {
            "implementation": "sklearn.ensemble.RandomForestRegressor",
            "sklearn_version": sklearn.__version__ if sklearn is not None else None,
            "selection_metric": "chronological validation RMSE",
            "tie_break_metric": "chronological validation QLIKE",
            "validation_fraction": self.config.validation_fraction,
            "tuning_candidate_count": len(self.tuning_rows_),
            "tuning_train_rows": self.tuning_train_rows_,
            "tuning_validation_rows": self.tuning_validation_rows_,
            "selected_hyperparameters": self.selected_params_,
            "resolved_max_features": self.resolved_max_features_,
            "oob_coverage": self.oob_coverage_,
            "oob_RMSE": self.oob_rmse_,
            "note": (
                "Candidates are compared only on the chronological tail of the "
                "training period; the selected configuration is refitted on all "
                "pre-test rows. The final test set is not used for tuning."
            ),
        }
