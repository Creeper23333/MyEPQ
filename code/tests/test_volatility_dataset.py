from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from epq_pipeline.config import FetchConfig
from epq_pipeline.data.volatility_dataset import (
    build_candle_quality_report,
    build_metadata,
    build_processed_rows,
    keep_completed_candles,
    validate_candles,
)


class VolatilityDatasetTests(unittest.TestCase):
    def test_candle_quality_report_checks_prices_order_and_activity(self) -> None:
        candles = [
            {"t": 0, "T": 86_399_999, "s": "BTC", "i": "1d", "o": "100", "h": "110", "l": "90", "c": "105", "v": "5", "n": 8},
            {"t": 86_400_000, "T": 172_799_999, "s": "BTC", "i": "1d", "o": "105", "h": "108", "l": "101", "c": "103", "v": "4", "n": 6},
        ]
        report = build_candle_quality_report(candles)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["critical_issue_count"], 0)
        self.assertEqual(report["unexpected_start_gap_rows"], 0)
        self.assertEqual(validate_candles(candles), report)

    def test_candle_quality_validation_rejects_daily_cadence_gap(self) -> None:
        candles = [
            {"t": 0, "T": 86_399_999, "s": "BTC", "i": "1d", "o": "100", "h": "110", "l": "90", "c": "105", "v": "5", "n": 8},
            {"t": 172_800_000, "T": 259_199_999, "s": "BTC", "i": "1d", "o": "105", "h": "108", "l": "101", "c": "103", "v": "4", "n": 6},
        ]
        report = build_candle_quality_report(candles)
        self.assertEqual(report["unexpected_start_gap_rows"], 1)
        with self.assertRaises(ValueError):
            validate_candles(candles)

    def test_candle_quality_validation_rejects_invalid_ohlc(self) -> None:
        bad = [
            {"t": 1000, "T": 1999, "s": "BTC", "i": "1d", "o": "100", "h": "99", "l": "90", "c": "105", "v": "5", "n": 8},
        ]
        with self.assertRaises(ValueError):
            validate_candles(bad)

    def test_keep_completed_candles_excludes_still_open_daily_row(self) -> None:
        candles = [
            {"T": 1000, "t": 0},
            {"T": 2000, "t": 1001},
        ]
        completed, excluded = keep_completed_candles(candles, as_of_ms=1500)
        self.assertEqual(completed, [candles[0]])
        self.assertEqual(excluded, 1)

    def test_build_processed_rows_generates_windowed_realised_volatility(self) -> None:
        candles = [
            {"t": 1704067200000, "T": 1704153599000, "s": "BTC", "i": "1d", "o": "100", "h": "100", "l": "100", "c": "100", "v": "10", "n": 1},
            {"t": 1704153600000, "T": 1704239999000, "s": "BTC", "i": "1d", "o": "110", "h": "110", "l": "110", "c": "110", "v": "12", "n": 2},
            {"t": 1704240000000, "T": 1704326399000, "s": "BTC", "i": "1d", "o": "121", "h": "121", "l": "121", "c": "121", "v": "14", "n": 3},
        ]
        rows = build_processed_rows(candles, window=2)
        self.assertIsNone(rows[0]["log_return"])
        self.assertAlmostEqual(rows[1]["log_return"], math.log(110 / 100), places=10)
        self.assertAlmostEqual(rows[2]["realised_volatility_2d"], 0.0, places=10)

    def test_build_metadata_records_request_window_and_role_check(self) -> None:
        config = FetchConfig(
            start_date="2026-01-01",
            end_date="2026-01-03",
            user_address="0x0000000000000000000000000000000000000000",
            raw_output=Path("data/raw/test.csv"),
            processed_output=Path("data/processed/test.csv"),
            metadata_output=Path("data/raw/test.json"),
        )
        candles = [
            {"t": 1704067200000, "T": 1704153599000, "s": "BTC", "i": "1d", "o": "100", "h": "100", "l": "100", "c": "100", "v": "10", "n": 1},
            {"t": 1704153600000, "T": 1704239999000, "s": "BTC", "i": "1d", "o": "110", "h": "110", "l": "110", "c": "110", "v": "12", "n": 2},
        ]
        metadata = build_metadata(config, start_ms=1, end_ms=2, candles=candles, user_role={"role": "user"})
        self.assertEqual(metadata["coin"], "BTC")
        self.assertEqual(metadata["rows"], 2)
        self.assertEqual(metadata["user_address_role_check"]["response"]["role"], "user")
        self.assertEqual(metadata["start_time_ms"], 1)
        self.assertEqual(metadata["end_time_ms"], 2)


if __name__ == "__main__":
    unittest.main()
