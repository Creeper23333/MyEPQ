from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.config import RandomForestConfig
from epq_pipeline.models.random_forest import SimpleRandomForestRegressor


class RandomForestTests(unittest.TestCase):
    def test_node_count_reports_fitted_forest_structure(self) -> None:
        x = np.arange(40, dtype=float).reshape(20, 2)
        y = np.linspace(0.01, 0.10, 20)
        model = SimpleRandomForestRegressor(
            RandomForestConfig(n_estimators=4, max_depth=3, min_samples_leaf=2),
            random_state=42,
        ).fit(x, y)
        self.assertGreaterEqual(model.node_count, 4)
        self.assertEqual(len(model.predict(x)), len(x))
        self.assertEqual(model.resolved_max_features_, 1)

    def test_oob_diagnostic_covers_training_rows(self) -> None:
        rng = np.random.default_rng(3)
        x = rng.normal(size=(80, 4))
        y = x[:, 0] * 0.5 + rng.normal(scale=0.05, size=80)
        model = SimpleRandomForestRegressor(
            RandomForestConfig(n_estimators=30, max_depth=4, min_samples_leaf=3),
            random_state=9,
        ).fit(x, y)
        self.assertIsNotNone(model.oob_predictions_)
        self.assertIsNotNone(model.oob_rmse_)
        self.assertGreater(model.oob_coverage_, 0.95)
        self.assertTrue(np.isfinite(model.oob_rmse_))

    def test_invalid_max_features_is_rejected(self) -> None:
        x = np.arange(30, dtype=float).reshape(10, 3)
        y = np.linspace(0.0, 1.0, 10)
        model = SimpleRandomForestRegressor(
            RandomForestConfig(
                n_estimators=2,
                max_depth=2,
                min_samples_leaf=2,
                max_features=4,
            ),
            random_state=1,
        )
        with self.assertRaisesRegex(ValueError, "max_features"):
            model.fit(x, y)


if __name__ == "__main__":
    unittest.main()
