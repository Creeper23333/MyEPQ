#!/usr/bin/env python3
"""Compare the current model results with an earlier data cut using one method.

The primary split is frozen, so appending completed candles should extend only
the test period.  This script truncates the current processed archive at a
chosen earlier date, reruns the same current implementations and hyperparameters,
then exports an apples-to-apples RMSE/rank comparison.  It does not reuse the
historical output files, which may have been produced by older code.
"""

from __future__ import annotations

import argparse
import csv
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from epq_pipeline.common.io import write_csv_rows  # noqa: E402
from epq_pipeline.config import ModelRunConfig  # noqa: E402
from epq_pipeline.pipeline.model_runner import evaluate_models, prepare_modelling_data  # noqa: E402


def read_current_performance(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["model"]: row for row in csv.DictReader(handle)}


def build_parser() -> argparse.ArgumentParser:
    default = ModelRunConfig()
    parser = argparse.ArgumentParser(
        description="Rerun the current method on an earlier data cut and compare it with the current output."
    )
    parser.add_argument("--input-path", type=Path, default=default.input_path)
    parser.add_argument("--current-performance", type=Path, default=default.performance_path)
    parser.add_argument("--comparison-end-date", default="2026-07-12")
    parser.add_argument("--test-start-date", default=default.test_start_date)
    parser.add_argument(
        "--output-path",
        type=Path,
        default=default.output_dir / "model_refresh_stability.csv",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    full = pd.read_csv(args.input_path, parse_dates=["date"])
    comparison_end = pd.Timestamp(args.comparison_end_date)
    earlier = full.loc[full["date"] <= comparison_end].copy()
    if earlier.empty or earlier["date"].iloc[-1] != comparison_end:
        raise ValueError("Comparison end date is not present in the processed archive")
    if len(earlier) == len(full):
        raise ValueError("Comparison cut must end before the current processed archive")

    current = read_current_performance(args.current_performance)
    current_end = str(full["date"].iloc[-1].date())
    with tempfile.TemporaryDirectory(prefix="epq-refresh-stability-") as directory:
        temporary_root = Path(directory)
        earlier_input = temporary_root / "processed_earlier_cut.csv"
        earlier.to_csv(earlier_input, index=False, lineterminator="\n", date_format="%Y-%m-%d")
        config = ModelRunConfig(
            input_path=earlier_input,
            output_dir=temporary_root / "outputs",
            test_start_date=args.test_start_date,
        )
        prepared = prepare_modelling_data(config)
        evaluation = evaluate_models(prepared, config)

    earlier_rows = {
        row.model: (rank, row.rmse)
        for rank, row in enumerate(evaluation.ranked_rows, start=1)
    }
    output_rows: list[dict[str, object]] = []
    for model, (earlier_rank, earlier_rmse) in earlier_rows.items():
        if model not in current:
            raise ValueError(f"Current performance output does not contain {model}")
        current_row = current[model]
        current_rmse = float(current_row["RMSE"])
        output_rows.append(
            {
                "model": model,
                "comparison_input_end": args.comparison_end_date,
                "current_input_end": current_end,
                "frozen_test_start": args.test_start_date,
                "comparison_test_rows": len(prepared.test),
                "current_rank": int(current_row["rank_by_RMSE"]),
                "comparison_rank": earlier_rank,
                "current_RMSE": f"{current_rmse:.8f}",
                "comparison_RMSE": f"{earlier_rmse:.8f}",
                "absolute_RMSE_change": f"{current_rmse - earlier_rmse:.8f}",
                "percent_RMSE_change": f"{((current_rmse / earlier_rmse) - 1.0) * 100.0:.3f}",
                "method_note": "Both columns use the current code, fixed cutoff, features and hyperparameters; only the data end date changes.",
            }
        )

    output_rows.sort(key=lambda row: int(row["current_rank"]))
    write_csv_rows(
        args.output_path,
        [
            "model",
            "comparison_input_end",
            "current_input_end",
            "frozen_test_start",
            "comparison_test_rows",
            "current_rank",
            "comparison_rank",
            "current_RMSE",
            "comparison_RMSE",
            "absolute_RMSE_change",
            "percent_RMSE_change",
            "method_note",
        ],
        output_rows,
    )
    print(f"Wrote {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
