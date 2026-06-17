#!/usr/bin/env python3
"""Fetch Hyperliquid BTC candle data and build a volatility-ready dataset.

The script uses Hyperliquid's public info endpoint. Market candles do not
require a user address. The supplied address can still be passed to
`--user-address` for a lightweight role check, but the forecasting dataset is
based on public exchange OHLCV data only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from datetime import UTC, date, datetime, time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.hyperliquid.xyz/info"
DEFAULT_COIN = "BTC"
DEFAULT_INTERVAL = "1d"
DEFAULT_START_DATE = "2023-02-26"
DEFAULT_WINDOW = 30
DEFAULT_USER_ADDRESS = "0x28e81E9fAC95AC1fae40870E4C08E6b94FcB1C23"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Hyperliquid candles and calculate rolling volatility.",
    )
    parser.add_argument("--coin", default=DEFAULT_COIN, help="Hyperliquid coin, e.g. BTC")
    parser.add_argument(
        "--interval",
        default=DEFAULT_INTERVAL,
        help="Candle interval, e.g. 1d, 1h, 15m",
    )
    parser.add_argument(
        "--start-date",
        default=DEFAULT_START_DATE,
        help="UTC start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end-date",
        default=datetime.now(UTC).date().isoformat(),
        help="UTC end date in YYYY-MM-DD format, inclusive",
    )
    parser.add_argument(
        "--window",
        default=DEFAULT_WINDOW,
        type=int,
        help="Rolling realised volatility window in candles",
    )
    parser.add_argument(
        "--user-address",
        default=DEFAULT_USER_ADDRESS,
        help="Optional Hyperliquid user address for metadata role check",
    )
    parser.add_argument(
        "--raw-output",
        default="data/raw/hyperliquid_BTC_1d_candles.csv",
        help="Raw OHLCV CSV output path",
    )
    parser.add_argument(
        "--processed-output",
        default="data/processed/hyperliquid_BTC_1d_volatility.csv",
        help="Processed volatility CSV output path",
    )
    parser.add_argument(
        "--metadata-output",
        default="data/raw/hyperliquid_BTC_1d_metadata.json",
        help="Metadata JSON output path",
    )
    return parser.parse_args()


def utc_ms(day: str, end_of_day: bool = False) -> int:
    parsed = date.fromisoformat(day)
    if end_of_day:
        dt = datetime.combine(parsed, time(23, 59, 59, 999000), tzinfo=UTC)
    else:
        dt = datetime.combine(parsed, time.min, tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def post_info(payload: dict[str, Any]) -> Any:
    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Hyperliquid API HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Hyperliquid API: {exc.reason}") from exc


def fetch_candles(coin: str, interval: str, start_ms: int, end_ms: int) -> list[dict[str, Any]]:
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": interval,
            "startTime": start_ms,
            "endTime": end_ms,
        },
    }
    candles = post_info(payload)
    if not isinstance(candles, list):
        raise RuntimeError(f"Unexpected candle response: {candles!r}")
    return sorted(candles, key=lambda row: int(row["t"]))


def user_role(user_address: str | None) -> Any:
    if not user_address:
        return None
    return post_info({"type": "userRole", "user": user_address})


def write_raw_candles(path: Path, candles: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
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
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
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


def build_processed_rows(
    candles: list[dict[str, Any]],
    window: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    closes = [float(row["c"]) for row in candles]
    returns: list[float | None] = [None]
    for index in range(1, len(closes)):
        returns.append(math.log(closes[index] / closes[index - 1]))

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
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "date",
        "close",
        "log_return",
        f"realised_volatility_{window}d",
        f"realised_volatility_{window}d_annualised",
        "volume",
        "trade_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_metadata(
    path: Path,
    args: argparse.Namespace,
    start_ms: int,
    end_ms: int,
    candles: list[dict[str, Any]],
    role: Any,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "source": "Hyperliquid public info API",
        "api_url": API_URL,
        "endpoint_type": "candleSnapshot",
        "coin": args.coin,
        "interval": args.interval,
        "start_date": args.start_date,
        "end_date": args.end_date,
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
        "rolling_volatility_window": args.window,
        "sample_note": "Default start date is 2023-02-26 because this pull shows earlier returned daily BTC candles with zero volume and zero trade count.",
        "user_address_role_check": {
            "address": args.user_address,
            "response": role,
            "note": "Market candles do not require a user address; this only records the optional address role.",
        }
        if args.user_address
        else None,
        "docs": {
            "official_info_endpoint": "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint",
            "official_rate_limits": "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits",
        },
        "fetched_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    start_ms = utc_ms(args.start_date)
    end_ms = utc_ms(args.end_date, end_of_day=True)
    if end_ms <= start_ms:
        print("end-date must be after start-date", file=sys.stderr)
        return 2

    candles = fetch_candles(args.coin, args.interval, start_ms, end_ms)
    if not candles:
        print("No candles returned by Hyperliquid API", file=sys.stderr)
        return 1

    role = user_role(args.user_address) if args.user_address else None

    raw_path = Path(args.raw_output)
    processed_path = Path(args.processed_output)
    metadata_path = Path(args.metadata_output)

    write_raw_candles(raw_path, candles)
    processed_rows = build_processed_rows(candles, args.window)
    write_processed_rows(processed_path, processed_rows, args.window)
    write_metadata(metadata_path, args, start_ms, end_ms, candles, role)

    print(f"Fetched {len(candles)} {args.coin} {args.interval} candles from Hyperliquid")
    print(f"Raw candles: {raw_path}")
    print(f"Processed volatility: {processed_path}")
    print(f"Metadata: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
