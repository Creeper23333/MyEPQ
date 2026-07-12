"""Hyperliquid client helpers."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from epq_pipeline.config import DEFAULT_TIMEOUT_SECONDS


def utc_ms(day: str, end_of_day: bool = False) -> int:
    parsed = date.fromisoformat(day)
    if end_of_day:
        dt = datetime.combine(parsed, time(23, 59, 59, 999000), tzinfo=UTC)
    else:
        dt = datetime.combine(parsed, time.min, tzinfo=UTC)
    return int(dt.timestamp() * 1000)


class HyperliquidClient:
    def __init__(self, api_url: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
        self.api_url = api_url
        self.timeout_seconds = timeout_seconds

    def post_info(self, payload: dict[str, Any]) -> Any:
        request = Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Hyperliquid API HTTP {exc.code}: {body}") from exc
        except URLError as exc:
            raise RuntimeError(f"Could not reach Hyperliquid API: {exc.reason}") from exc

    def fetch_candles(self, coin: str, interval: str, start_ms: int, end_ms: int) -> list[dict[str, Any]]:
        payload = {
            "type": "candleSnapshot",
            "req": {
                "coin": coin,
                "interval": interval,
                "startTime": start_ms,
                "endTime": end_ms,
            },
        }
        candles = self.post_info(payload)
        if not isinstance(candles, list):
            raise RuntimeError(f"Unexpected candle response: {candles!r}")
        return sorted(candles, key=lambda row: int(row["t"]))

    def fetch_user_role(self, user_address: str | None) -> Any:
        if not user_address:
            return None
        return self.post_info({"type": "userRole", "user": user_address})

