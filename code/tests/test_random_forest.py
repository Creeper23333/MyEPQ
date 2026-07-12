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


if __name__ == "__main__":
    unittest.main()
