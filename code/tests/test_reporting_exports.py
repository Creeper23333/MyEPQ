from __future__ import annotations

import hashlib
import sys
import tempfile
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
                "target_date": pd.to_datetime(["2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]),
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
        self.assertIn(str(self.config.garch_conversion_sensitivity_path), summary)
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
        self.assertEqual(metadata["validation_design"], "frozen forecast-origin cutoff")
        self.assertEqual(metadata["split_cutoff"], "2025-11-16")
        self.assertEqual(metadata["train_window"]["rows"], 3)
        self.assertIn(
            "code/outputs/garch_target_conversion_sensitivity.csv",
            metadata["generated_outputs"],
        )

    def test_run_metadata_records_input_checksum_versions_and_effective_samples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "processed.csv"
            input_path.write_bytes(b"date,close\n2026-01-01,1\n")
            config = ModelRunConfig(input_path=input_path, output_dir=Path(directory) / "outputs")
            metadata = build_run_metadata(
                config,
                raw_dataset=self.frame,
                frame=self.frame,
                train=self.train,
                test=self.test,
                garch_params={
                    "alpha": 0.1,
                    "beta": 0.8,
                    "omega": 0.01,
                    "training_observations": 77,
                },
                lstm_metadata={
                    "status": "trained",
                    "train_sequences": 10,
                    "validation_sequences": 2,
                    "train_sequences_total": 12,
                    "torch_version": "test-version",
                },
                resolved_rf_max_features=5,
            )
            self.assertEqual(
                metadata["processed_input"]["sha256"],
                hashlib.sha256(input_path.read_bytes()).hexdigest(),
            )
            self.assertEqual(
                metadata["random_forest_hyperparameters"]["resolved_max_features"],
                5,
            )
            self.assertEqual(
                metadata["effective_training_samples"]["GARCH(1,1)"]["finite_return_rows"],
                77,
            )
            self.assertEqual(
                metadata["effective_training_samples"]["LSTM"]["parameter_fit_sequences"],
                10,
            )
            self.assertIn("python", metadata["runtime_versions"])
            self.assertIn("numpy", metadata["runtime_versions"])


if __name__ == "__main__":
    unittest.main()
