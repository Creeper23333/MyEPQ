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
) -> dict[str, Any]:
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
        "rows": len(candles),
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
        "fetched_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }


def refresh_hyperliquid_dataset(config: FetchConfig, client: HyperliquidClient | None = None) -> dict[str, Any]:
    start_ms = utc_ms(config.start_date)
    end_ms = utc_ms(config.end_date, end_of_day=True)
    if end_ms <= start_ms:
        raise ValueError("end-date must be after start-date")

    client = client or HyperliquidClient(config.api_url, timeout_seconds=config.timeout_seconds)
    candles = client.fetch_candles(config.coin, config.interval, start_ms, end_ms)
    if not candles:
        raise ValueError("No candles returned by Hyperliquid API")

    user_role = client.fetch_user_role(config.user_address)
    processed_rows = build_processed_rows(candles, config.window)
    metadata = build_metadata(config, start_ms, end_ms, candles, user_role)

    write_raw_candles(config.raw_output, candles)
    write_processed_rows(config.processed_output, processed_rows, config.window)
    write_json(config.metadata_output, metadata)

    return {
        "candle_count": len(candles),
        "raw_output": config.raw_output,
        "processed_output": config.processed_output,
        "metadata_output": config.metadata_output,
        "metadata": metadata,
    }

