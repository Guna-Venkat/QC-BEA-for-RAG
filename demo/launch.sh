#!/usr/bin/env bash
set -eu
DEMO_BUNDLE="$(cd "$(dirname "$0")" && pwd)"
if [ -n "${DEMO_PYTHON:-}" ]; then
  reader_python="$DEMO_PYTHON"
elif [ -x "$DEMO_BUNDLE/../.venv/bin/python" ]; then
  reader_python="$DEMO_BUNDLE/../.venv/bin/python"
elif [ -x "$DEMO_BUNDLE/.venv/bin/python" ]; then
  reader_python="$DEMO_BUNDLE/.venv/bin/python"
elif [ -x "$DEMO_BUNDLE/../../demo/.venv/bin/python" ]; then
  reader_python="$DEMO_BUNDLE/../../demo/.venv/bin/python"
else
  reader_python=python3
fi
cd "$DEMO_BUNDLE/application"
export PYTHONDONTWRITEBYTECODE=1
exec "$reader_python" -m streamlit run "$DEMO_BUNDLE/app.py" "$@"
