#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
END_DATE="${1:-${EPQ_END_DATE:-$(date +%F)}}"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing .venv Python. Run: python3 -m venv .venv && .venv/bin/python -m pip install -r code/requirements.txt" >&2
  exit 1
fi

"$PYTHON_BIN" "$ROOT_DIR/code/fetch_hyperliquid_data.py" --end-date "$END_DATE"
"$PYTHON_BIN" "$ROOT_DIR/code/run_volatility_models.py"
