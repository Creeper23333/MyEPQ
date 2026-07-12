#!/usr/bin/env python3
"""Backwards-compatible wrapper for the packaged modelling pipeline."""

from __future__ import annotations

from epq_pipeline.pipeline.model_runner import main


if __name__ == "__main__":
    raise SystemExit(main())
