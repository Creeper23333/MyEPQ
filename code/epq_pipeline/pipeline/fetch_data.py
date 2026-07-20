"""CLI orchestration for the data-fetch pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from epq_pipeline.config import FetchConfig
from epq_pipeline.data.volatility_dataset import refresh_hyperliquid_dataset


def build_arg_parser() -> argparse.ArgumentParser:
    default_config = FetchConfig()
    parser = argparse.ArgumentParser(
        description="Fetch Hyperliquid candles and calculate rolling volatility.",
    )
    parser.add_argument("--coin", default=default_config.coin, help="Hyperliquid coin, e.g. BTC")
    parser.add_argument("--interval", default=default_config.interval, help="Candle interval, e.g. 1d, 1h, 15m")
    parser.add_argument("--start-date", default=default_config.start_date, help="UTC start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", default=default_config.end_date, help="UTC end date in YYYY-MM-DD format, inclusive")
    parser.add_argument("--window", default=default_config.window, type=int, help="Rolling realised volatility window in candles")
    parser.add_argument("--user-address", default=default_config.user_address, help="Optional Hyperliquid user address for metadata role check")
    parser.add_argument("--raw-output", default=str(default_config.raw_output), help="Raw OHLCV CSV output path")
    parser.add_argument("--processed-output", default=str(default_config.processed_output), help="Processed volatility CSV output path")
    parser.add_argument("--metadata-output", default=str(default_config.metadata_output), help="Metadata JSON output path")
    parser.add_argument("--quality-output", default=str(default_config.quality_output), help="Data-quality JSON output path")
    return parser


def config_from_args(args: argparse.Namespace) -> FetchConfig:
    return FetchConfig(
        coin=args.coin,
        interval=args.interval,
        start_date=args.start_date,
        end_date=args.end_date,
        window=args.window,
        user_address=args.user_address,
        raw_output=Path(args.raw_output),
        processed_output=Path(args.processed_output),
        metadata_output=Path(args.metadata_output),
        quality_output=Path(args.quality_output),
    )


def run_fetch_command(args: argparse.Namespace) -> int:
    config = config_from_args(args)
    try:
        result = refresh_hyperliquid_dataset(config)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Fetched {result['candle_count']} {config.coin} {config.interval} candles from Hyperliquid")
    print(f"Raw candles: {result['raw_output']}")
    print(f"Processed volatility: {result['processed_output']}")
    print(f"Metadata: {result['metadata_output']}")
    print(f"Quality report: {result['quality_output']}")
    return 0


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    return run_fetch_command(args)


if __name__ == "__main__":
    raise SystemExit(main())
