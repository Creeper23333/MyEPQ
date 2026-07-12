#!/usr/bin/env python3
"""Backwards-compatible wrapper for the packaged data-fetch pipeline."""

from __future__ import annotations

from epq_pipeline.pipeline.fetch_data import main


if __name__ == "__main__":
    raise SystemExit(main())
