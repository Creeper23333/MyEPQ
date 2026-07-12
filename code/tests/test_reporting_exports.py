from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.common.types import PerformanceRow
from epq_pipeline.config import ModelRunConfig
from epq_pipeline.reporting.exports import build_model_summary_markdown, build_run_metadata


class ReportingExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = ModelRunConfig(
            input_path=Path("data/processed/sample.csv"),
            output_dir=Path("code/outputs"),
        )
        self.frame = pd.DataFrame(
            {
                "date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]),
                self.config.target_col: [0.1, 0.2, 0.3, 0.4],
            }
        )
        self.train = self.frame.iloc[:3].copy()
        self.test = self.frame.iloc[3:].copy()
        self.ranked_rows = [
            PerformanceRow("Lagged linear regression", "Interpretable lag-feature model", 0.1, 0.02, 0.14),
            PerformanceRow("Rolling historical volatility", "Benchmark", 0.2, 0.04, 0.20),
        ]

    def test_model_summary_lists_all_generated_output_files(self) -> None:
        summary = build_model_summary_markdown(
            self.config,
            self.frame,
            self.train,
            self.test,
            self.ranked_rows,
            {"status": "trained", "epochs_trained": 12},
        )
        self.assertIn(str(self.config.linear_coefficients_path), summary)
        self.assertIn(str(self.config.run_metadata_path), summary)
        self.assertIn(str(self.config.multidimensional_comparison_path), summary)
        self.assertIn(str(self.config.robustness_path), summary)
        self.assertIn(str(self.config.summary_path), summary)

    def test_run_metadata_includes_generated_outputs(self) -> None:
        metadata = build_run_metadata(
            self.config,
            raw_dataset=self.frame,
            frame=self.frame,
            train=self.train,
            test=self.test,
            garch_params={"alpha": 0.1, "beta": 0.8, "omega": 0.01},
            lstm_metadata={"status": "trained"},
        )
        self.assertIn("generated_outputs", metadata)
        self.assertIn("code/outputs/model_run_metadata.json", metadata["generated_outputs"])
        self.assertIn("code/outputs/model_multidimensional_comparison.csv", metadata["generated_outputs"])
        self.assertEqual(metadata["validation_design"], "fixed chronological holdout")
        self.assertEqual(metadata["train_window"]["rows"], 3)


if __name__ == "__main__":
    unittest.main()
