"""Dataset construction for the Hyperliquid BTC volatility study."""

from __future__ import annotations

import csv
import math
import statistics
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from epq_pipeline.common.io import ensure_parent_directory, write_json
from epq_pipeline.config import FetchConfig
from epq_pipeline.data.hyperliquid import HyperliquidClient, utc_ms


def keep_completed_candles(
    candles: list[dict[str, Any]],
    as_of_ms: int,
) -> tuple[list[dict[str, Any]], int]:
    """Exclude a still-open candle whose advertised end time is in the future."""
    completed = [row for row in candles if int(row["T"]) < as_of_ms]
    return completed, len(candles) - len(completed)


def build_candle_quality_report(candles: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate schema, ordering, prices and activity before modelling."""
    required = {"t", "T", "s", "i", "o", "h", "l", "c", "v", "n"}
    missing_field_rows = sum(not required.issubset(row) for row in candles)
    if missing_field_rows:
        raise ValueError(f"{missing_field_rows} candle rows are missing required fields")

    starts = [int(row["t"]) for row in candles]
    ends = [int(row["T"]) for row in candles]
    opens = [float(row["o"]) for row in candles]
    highs = [float(row["h"]) for row in candles]
    lows = [float(row["l"]) for row in candles]
    closes = [float(row["c"]) for row in candles]
    volumes = [float(row["v"]) for row in candles]
    trades = [int(row["n"]) for row in candles]
    symbols = [str(row["s"]) for row in candles]
    intervals = [str(row["i"]) for row in candles]

    duplicate_start_timestamps = len(starts) - len(set(starts))
    non_increasing_starts = sum(current <= previous for previous, current in zip(starts, starts[1:]))
    invalid_timestamp_ranges = sum(end <= start for start, end in zip(starts, ends))
    nonpositive_prices = sum(
        any(value <= 0.0 for value in values)
        for values in zip(opens, highs, lows, closes)
    )
    invalid_ohlc_rows = sum(
        not (low <= min(open_price, close) <= max(open_price, close) <= high)
        for open_price, high, low, close in zip(opens, highs, lows, closes)
    )
    negative_volume_rows = sum(value < 0.0 for value in volumes)
    negative_trade_count_rows = sum(value < 0 for value in trades)
    zero_volume_rows = sum(value == 0.0 for value in volumes)
    zero_trade_count_rows = sum(value == 0 for value in trades)
    distinct_symbols = sorted(set(symbols))
    distinct_intervals = sorted(set(intervals))
    inconsistent_symbol_series = int(len(distinct_symbols) > 1)
    inconsistent_interval_series = int(len(distinct_intervals) > 1)
    interval_ms = {
        "1m": 60_000,
        "3m": 180_000,
        "5m": 300_000,
        "15m": 900_000,
        "30m": 1_800_000,
        "1h": 3_600_000,
        "2h": 7_200_000,
        "4h": 14_400_000,
        "8h": 28_800_000,
        "12h": 43_200_000,
        "1d": 86_400_000,
    }
    expected_start_gap_ms = (
        interval_ms.get(distinct_intervals[0])
        if len(distinct_intervals) == 1
        else None
    )
    observed_start_gaps = [current - previous for previous, current in zip(starts, starts[1:])]
    unexpected_start_gap_rows = (
        sum(gap != expected_start_gap_ms for gap in observed_start_gaps)
        if expected_start_gap_ms is not None
        else 0
    )

    critical_issue_count = sum(
        [
            duplicate_start_timestamps,
            non_increasing_starts,
            invalid_timestamp_ranges,
            nonpositive_prices,
            invalid_ohlc_rows,
            negative_volume_rows,
            negative_trade_count_rows,
            inconsistent_symbol_series,
            inconsistent_interval_series,
            unexpected_start_gap_rows,
        ]
    )
    return {
        "status": "passed" if critical_issue_count == 0 else "failed",
        "rows_checked": len(candles),
        "missing_required_field_rows": missing_field_rows,
        "duplicate_start_timestamps": duplicate_start_timestamps,
        "non_increasing_start_timestamps": non_increasing_starts,
        "invalid_timestamp_ranges": invalid_timestamp_ranges,
        "nonpositive_price_rows": nonpositive_prices,
        "invalid_ohlc_rows": invalid_ohlc_rows,
        "negative_volume_rows": negative_volume_rows,
        "negative_trade_count_rows": negative_trade_count_rows,
        "zero_volume_rows": zero_volume_rows,
        "zero_trade_count_rows": zero_trade_count_rows,
        "distinct_symbols": distinct_symbols,
        "distinct_intervals": distinct_intervals,
        "inconsistent_symbol_series": inconsistent_symbol_series,
        "inconsistent_interval_series": inconsistent_interval_series,
        "expected_start_gap_ms": expected_start_gap_ms,
        "minimum_observed_start_gap_ms": min(observed_start_gaps) if observed_start_gaps else None,
        "maximum_observed_start_gap_ms": max(observed_start_gaps) if observed_start_gaps else None,
        "unexpected_start_gap_rows": unexpected_start_gap_rows,
        "critical_issue_count": critical_issue_count,
        "note": "Zero activity is reported but not automatically rejected; critical schema, timestamp, cadence, symbol, interval, price and negative-activity issues stop the refresh.",
    }


def validate_candles(candles: list[dict[str, Any]]) -> dict[str, Any]:
    report = build_candle_quality_report(candles)
    if report["critical_issue_count"]:
        raise ValueError(f"Candle quality validation failed: {report}")
    return report


def write_raw_candles(path: Path, candles: list[dict[str, Any]]) -> None:
    ensure_parent_directory(path)
    fieldnames = [
        "timestamp_start_ms",
        "timestamp_end_ms",
        "date",
        "symbol",
        "interval",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "trade_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in candles:
            start_ms = int(row["t"])
            writer.writerow(
                {
                    "timestamp_start_ms": start_ms,
                    "timestamp_end_ms": int(row["T"]),
                    "date": datetime.fromtimestamp(start_ms / 1000, UTC).date().isoformat(),
                    "symbol": row["s"],
                    "interval": row["i"],
                    "open": row["o"],
                    "high": row["h"],
                    "low": row["l"],
                    "close": row["c"],
                    "volume": row["v"],
                    "trade_count": row["n"],
                }
            )


def build_processed_rows(candles: list[dict[str, Any]], window: int) -> list[dict[str, Any]]:
    closes = [float(row["c"]) for row in candles]
    returns: list[float | None] = [None]
    for index in range(1, len(closes)):
        returns.append(math.log(closes[index] / closes[index - 1]))

    rows: list[dict[str, Any]] = []
    for index, row in enumerate(candles):
        log_return = returns[index]
        rv_window = returns[index - window + 1 : index + 1]
        realised = None
        if len(rv_window) == window and all(value is not None for value in rv_window):
            realised = statistics.stdev(value for value in rv_window if value is not None)
        start_ms = int(row["t"])
        rows.append(
            {
                "date": datetime.fromtimestamp(start_ms / 1000, UTC).date().isoformat(),
                "close": float(row["c"]),
                "log_return": log_return,
                f"realised_volatility_{window}d": realised,
                f"realised_volatility_{window}d_annualised": (
                    realised * math.sqrt(365) if realised is not None else None
                ),
                "volume": float(row["v"]),
                "trade_count": int(row["n"]),
            }
        )
    return rows


def write_processed_rows(path: Path, rows: list[dict[str, Any]], window: int) -> None:
    ensure_parent_directory(path)
    fieldnames = [
        "date",
        "close",
        "log_return",
        f"realised_volatility_{window}d",
        f"realised_volatility_{window}d_annualised",
        "volume",
        "trade_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_metadata(
    config: FetchConfig,
    start_ms: int,
    end_ms: int,
    candles: list[dict[str, Any]],
    user_role: Any,
    returned_rows: int | None = None,
    excluded_incomplete_rows: int = 0,
    fetched_at_utc: datetime | None = None,
) -> dict[str, Any]:
    fetched_at_utc = fetched_at_utc or datetime.now(UTC).replace(microsecond=0)
    return {
        "source": "Hyperliquid public info API",
        "api_url": config.api_url,
        "endpoint_type": "candleSnapshot",
        "coin": config.coin,
        "interval": config.interval,
        "start_date": config.start_date,
        "end_date": config.end_date,
        "start_time_ms": start_ms,
        "end_time_ms": end_ms,
        "rows_returned_by_api": returned_rows if returned_rows is not None else len(candles),
        "rows": len(candles),
        "incomplete_rows_excluded": excluded_incomplete_rows,
        "first_candle_date": (
            datetime.fromtimestamp(int(candles[0]["t"]) / 1000, UTC).date().isoformat()
            if candles
            else None
        ),
        "last_candle_date": (
            datetime.fromtimestamp(int(candles[-1]["t"]) / 1000, UTC).date().isoformat()
            if candles
            else None
        ),
        "rolling_volatility_window": config.window,
        "sample_note": "Default start date is 2023-02-26 because this pull shows earlier returned daily BTC candles with zero volume and zero trade count.",
        "user_address_role_check": {
            "address": config.user_address,
            "response": user_role,
            "note": "Market candles do not require a user address; this only records the optional address role.",
        }
        if config.user_address
        else None,
        "docs": {
            "official_info_endpoint": "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint",
            "official_rate_limits": "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits",
        },
        "fetched_at_utc": fetched_at_utc.isoformat(),
    }


def refresh_hyperliquid_dataset(config: FetchConfig, client: HyperliquidClient | None = None) -> dict[str, Any]:
    start_ms = utc_ms(config.start_date)
    end_ms = utc_ms(config.end_date, end_of_day=True)
    if end_ms <= start_ms:
        raise ValueError("end-date must be after start-date")

    client = client or HyperliquidClient(config.api_url, timeout_seconds=config.timeout_seconds)
    returned_candles = client.fetch_candles(config.coin, config.interval, start_ms, end_ms)
    if not returned_candles:
        raise ValueError("No candles returned by Hyperliquid API")

    fetched_at_utc = datetime.now(UTC).replace(microsecond=0)
    candles, excluded_incomplete_rows = keep_completed_candles(
        returned_candles,
        int(fetched_at_utc.timestamp() * 1000),
    )
    if not candles:
        raise ValueError("No completed candles returned by Hyperliquid API")
    quality_report = validate_candles(candles)

    user_role = client.fetch_user_role(config.user_address)
    processed_rows = build_processed_rows(candles, config.window)
    metadata = build_metadata(
        config,
        start_ms,
        end_ms,
        candles,
        user_role,
        returned_rows=len(returned_candles),
        excluded_incomplete_rows=excluded_incomplete_rows,
        fetched_at_utc=fetched_at_utc,
    )

    write_raw_candles(config.raw_output, candles)
    write_processed_rows(config.processed_output, processed_rows, config.window)
    write_json(config.metadata_output, metadata)
    write_json(config.quality_output, quality_report)

    return {
        "candle_count": len(candles),
        "raw_output": config.raw_output,
        "processed_output": config.processed_output,
        "metadata_output": config.metadata_output,
        "quality_output": config.quality_output,
        "metadata": metadata,
        "quality_report": quality_report,
    }
