from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.config import RandomForestConfig
from epq_pipeline.models.random_forest import StandardRandomForestRegressor


class RandomForestTests(unittest.TestCase):
    def test_node_count_reports_fitted_forest_structure(self) -> None:
        x = np.arange(80, dtype=float).reshape(40, 2)
        y = np.linspace(0.01, 0.10, 40)
        model = StandardRandomForestRegressor(
            RandomForestConfig(
                n_estimators=20,
                max_depth=3,
                min_samples_leaf=2,
                tune_hyperparameters=False,
            ),
            random_state=42,
        ).fit(x, y)
        self.assertGreaterEqual(model.node_count, 20)
        self.assertEqual(len(model.predict(x)), len(x))
        self.assertEqual(model.resolved_max_features_, 1)
        self.assertEqual(
            model.metadata["implementation"],
            "sklearn.ensemble.RandomForestRegressor",
        )

    def test_oob_diagnostic_covers_training_rows(self) -> None:
        rng = np.random.default_rng(3)
        x = rng.normal(size=(80, 4))
        y = x[:, 0] * 0.5 + rng.normal(scale=0.05, size=80)
        model = StandardRandomForestRegressor(
            RandomForestConfig(
                n_estimators=60,
                max_depth=4,
                min_samples_leaf=3,
                tune_hyperparameters=False,
            ),
            random_state=9,
        ).fit(x, y)
        self.assertIsNotNone(model.oob_predictions_)
        self.assertIsNotNone(model.oob_rmse_)
        self.assertGreater(model.oob_coverage_, 0.95)
        self.assertTrue(np.isfinite(model.oob_rmse_))

    def test_invalid_max_features_is_rejected(self) -> None:
        x = np.arange(30, dtype=float).reshape(10, 3)
        y = np.linspace(0.0, 1.0, 10)
        model = StandardRandomForestRegressor(
            RandomForestConfig(
                n_estimators=2,
                max_depth=2,
                min_samples_leaf=2,
                max_features=4,
                tune_hyperparameters=False,
            ),
            random_state=1,
        )
        with self.assertRaisesRegex(ValueError, "max_features"):
            model.fit(x, y)

    def test_tuning_uses_chronological_training_validation(self) -> None:
        rng = np.random.default_rng(11)
        x = rng.normal(size=(100, 3))
        y = 0.2 + x[:, 0] ** 2 + rng.normal(scale=0.02, size=100)
        model = StandardRandomForestRegressor(
            RandomForestConfig(
                n_estimators=30,
                validation_fraction=0.2,
                tuning_candidates=((2, 2, "sqrt"), (None, 2, "sqrt")),
            ),
            random_state=5,
        ).fit(x, y)
        self.assertEqual(len(model.tuning_rows_), 2)
        self.assertEqual(sum(bool(row["selected"]) for row in model.tuning_rows_), 1)
        self.assertEqual(model.tuning_train_rows_, 80)
        self.assertEqual(model.tuning_validation_rows_, 20)
        self.assertEqual(model.metadata["tuning_candidate_count"], 2)


if __name__ == "__main__":
    unittest.main()
