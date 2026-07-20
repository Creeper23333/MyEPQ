#!/usr/bin/env python3
"""Cross-check the final EPQ evidence bundle after a data/model refresh.

This is deliberately separate from the model unit tests.  It checks that the
generated data, predictions, metrics and canonical documents all describe the
same run, and that the English/Chinese production-log editions retain the same
structural identifiers and completion placeholders.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MODEL_COLUMNS = {
    "Rolling historical volatility": "rolling_historical",
    "GARCH(1,1)": "garch_1_1",
    "Lagged linear regression": "lagged_linear_regression",
    "Random Forest": "random_forest",
    "LSTM": "lstm",
}


@dataclass
class Audit:
    checks: int = 0
    failures: list[str] | None = None

    def __post_init__(self) -> None:
        if self.failures is None:
            self.failures = []

    def require(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            assert self.failures is not None
            self.failures.append(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def audit_data(root: Path, audit: Audit) -> tuple[dict[str, Any], dict[str, Any]]:
    fetch_metadata = load_json(root / "data/raw/hyperliquid_BTC_1d_metadata.json")
    quality = load_json(root / "data/raw/hyperliquid_BTC_1d_quality_report.json")
    raw_rows = load_csv(root / "data/raw/hyperliquid_BTC_1d_candles.csv")
    processed_rows = load_csv(root / "data/processed/hyperliquid_BTC_1d_volatility.csv")

    audit.require(quality.get("status") == "passed", "Data-quality status is not passed")
    audit.require(int(quality.get("critical_issue_count", -1)) == 0, "Data-quality report has critical issues")
    audit.require(len(raw_rows) == int(fetch_metadata["rows"]), "Raw CSV row count differs from fetch metadata")
    audit.require(len(processed_rows) == int(fetch_metadata["rows"]), "Processed CSV row count differs from fetch metadata")
    audit.require(raw_rows[-1]["date"] == fetch_metadata["last_candle_date"], "Raw CSV end date differs from fetch metadata")
    audit.require(processed_rows[-1]["date"] == fetch_metadata["last_candle_date"], "Processed CSV end date differs from fetch metadata")
    audit.require(len({row["date"] for row in processed_rows}) == len(processed_rows), "Processed dates are not unique")
    return fetch_metadata, quality


def audit_predictions(root: Path, audit: Audit) -> tuple[dict[str, Any], dict[str, float]]:
    outputs = root / "code/outputs"
    run_metadata = load_json(outputs / "model_run_metadata.json")
    predictions = load_csv(outputs / "model_predictions.csv")
    performance = load_csv(outputs / "model_performance.csv")
    processed_path = root / run_metadata["input_path"]

    processed_input = run_metadata.get("processed_input", {})
    recorded_checksum = (
        run_metadata.get("input_sha256")
        or run_metadata.get("input_file_sha256")
        or processed_input.get("sha256")
    )
    if recorded_checksum is not None:
        audit.require(recorded_checksum == sha256(processed_path), "Processed input SHA-256 differs from model metadata")

    test_window = run_metadata["test_window"]
    audit.require(len(predictions) == int(test_window["rows"]), "Prediction row count differs from test metadata")
    audit.require(predictions[0]["date"] == test_window["forecast_origin_start_date"], "Prediction start date differs from metadata")
    audit.require(predictions[-1]["date"] == test_window["forecast_origin_end_date"], "Prediction end date differs from metadata")
    audit.require(predictions[0]["target_date"] == test_window["target_start_date"], "Target start date differs from metadata")
    audit.require(predictions[-1]["target_date"] == test_window["target_end_date"], "Target end date differs from metadata")

    actual = [float(row["actual"]) for row in predictions]
    generated_metrics: dict[str, float] = {}
    rows_by_model = {row["model"]: row for row in performance}
    for model, column in MODEL_COLUMNS.items():
        if column not in predictions[0]:
            continue
        forecast = [float(row[column]) for row in predictions]
        errors = [observed - predicted for observed, predicted in zip(actual, forecast)]
        mae = mean([abs(value) for value in errors])
        mse = mean([value * value for value in errors])
        rmse = math.sqrt(mse)
        generated_metrics[model] = rmse
        audit.require(all(math.isfinite(value) for value in forecast), f"{model} predictions contain non-finite values")
        audit.require(model in rows_by_model, f"{model} is absent from model_performance.csv")
        if model in rows_by_model:
            row = rows_by_model[model]
            audit.require(abs(float(row["MAE"]) - mae) <= 5e-9, f"{model} MAE does not recompute")
            audit.require(abs(float(row["MSE"]) - mse) <= 5e-9, f"{model} MSE does not recompute")
            audit.require(abs(float(row["RMSE"]) - rmse) <= 5e-9, f"{model} RMSE does not recompute")

    ranked_models = [row["model"] for row in sorted(performance, key=lambda row: int(row["rank_by_RMSE"]))]
    recomputed_rank = sorted(generated_metrics, key=generated_metrics.get)
    audit.require(ranked_models == recomputed_rank, "Exported RMSE ranking differs from recomputed ranking")
    return run_metadata, generated_metrics


def audit_walk_forward(root: Path, audit: Audit) -> None:
    outputs = root / "code/outputs"
    primary = load_csv(outputs / "model_predictions.csv")
    rolling = load_csv(outputs / "model_walk_forward_predictions.csv")
    audit.require(len(rolling) == len(primary), "Walk-forward predictions do not cover the full primary test")
    audit.require(
        [row["target_date"] for row in rolling] == [row["target_date"] for row in primary],
        "Walk-forward target dates differ from or reorder the primary test",
    )
    audit.require(len({row["target_date"] for row in rolling}) == len(rolling), "Walk-forward target dates are duplicated")


def audit_documents(
    root: Path,
    audit: Audit,
    fetch_metadata: dict[str, Any],
    run_metadata: dict[str, Any],
    metrics: dict[str, float],
) -> None:
    canonical = [
        root / "README.md",
        root / "appendix/model-results-summary.md",
        root / "report/final-report.md",
        root / "zh-cn/README.md",
        root / "zh-cn/final-report-zh-cn.md",
    ]
    latest_date = str(fetch_metadata["last_candle_date"])
    garch_rmse = f"{metrics['GARCH(1,1)']:.8f}"
    test_rows = str(run_metadata["test_window"]["rows"])
    for path in canonical:
        text = path.read_text(encoding="utf-8")
        audit.require(latest_date in text, f"{path.relative_to(root)} lacks current last-candle date {latest_date}")
        audit.require(garch_rmse in text, f"{path.relative_to(root)} lacks current GARCH RMSE {garch_rmse}")
        audit.require(test_rows in text, f"{path.relative_to(root)} lacks current test count {test_rows}")
        audit.require("CURRENT_" not in text, f"{path.relative_to(root)} still contains a CURRENT_ placeholder")


def ordered_section_ids(text: str) -> list[str]:
    return re.findall(r"^##\s+(PL-\d{2})\b", text, flags=re.MULTILINE)


def ordered_placeholders(text: str) -> list[str]:
    return re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)


def audit_bilingual_log(root: Path, audit: Audit) -> None:
    english_path = root / "production-log/complete-production-log-en.md"
    chinese_path = root / "zh-cn/complete-production-log-zh-cn.md"
    audit.require(english_path.exists(), "Complete English production log is missing")
    audit.require(chinese_path.exists(), "Complete Chinese production log is missing")
    if not english_path.exists() or not chinese_path.exists():
        return
    english = english_path.read_text(encoding="utf-8")
    chinese = chinese_path.read_text(encoding="utf-8")
    audit.require(ordered_section_ids(english) == ordered_section_ids(chinese), "Bilingual log section IDs/order differ")
    audit.require(ordered_placeholders(english) == ordered_placeholders(chinese), "Bilingual log placeholder sequence differs")
    audit.require("CURRENT_" not in english and "CURRENT_" not in chinese, "Bilingual log still contains a CURRENT_ placeholder")
    generated_documents = (
        root / "production-log/complete-production-log-en.docx",
        root / "zh-cn/complete-production-log-zh-cn.docx",
    )
    for path in generated_documents:
        audit.require(path.exists() and path.stat().st_size > 1000, f"Generated document {path.name} is missing or unexpectedly small")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify that the EPQ evidence bundle describes one consistent run.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    audit = Audit()
    try:
        fetch_metadata, _quality = audit_data(root, audit)
        run_metadata, metrics = audit_predictions(root, audit)
        audit_walk_forward(root, audit)
        audit_documents(root, audit, fetch_metadata, run_metadata, metrics)
        audit_bilingual_log(root, audit)
    except (FileNotFoundError, KeyError, ValueError, IndexError, json.JSONDecodeError) as exc:
        assert audit.failures is not None
        audit.failures.append(f"Audit could not complete: {exc}")

    if audit.failures:
        print(f"EPQ bundle audit FAILED: {len(audit.failures)} issue(s) across {audit.checks} checks")
        for failure in audit.failures:
            print(f"- {failure}")
        return 1
    print(f"EPQ bundle audit PASSED: {audit.checks} consistency checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
