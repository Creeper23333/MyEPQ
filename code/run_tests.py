#!/usr/bin/env python3
"""Run the EPQ unit test suite from the project-local code directory."""

from __future__ import annotations

import unittest
from pathlib import Path


def main() -> int:
    test_dir = Path(__file__).with_name("tests")
    suite = unittest.defaultTestLoader.discover(str(test_dir), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
