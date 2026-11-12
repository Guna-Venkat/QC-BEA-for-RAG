#!/usr/bin/env bash
# Installs software only: no checkpoint downloads, inference or research execution.
set -eu
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_PYTHON="${PYTHON:-python3.11}"
MODE="${1:---saved}"
case "$MODE" in
  --saved) REQUIREMENTS=requirements.txt ;;
  --live) REQUIREMENTS=requirements-live.txt ;;
  --dev) REQUIREMENTS=requirements-dev.txt ;;
  *) echo "Usage: bash setup_demo.sh [--saved|--live|--dev]" >&2; exit 2 ;;
esac
"$REPO_PYTHON" -c 'import sys; assert sys.version_info[:2] == (3,11), "Use Python 3.11"'
if [ ! -x "$REPO_ROOT/.venv/bin/python" ]; then
  "$REPO_PYTHON" -m venv "$REPO_ROOT/.venv"
fi
"$REPO_ROOT/.venv/bin/python" -m pip install -r "$REPO_ROOT/$REQUIREMENTS"
"$REPO_ROOT/.venv/bin/python" -m pip check
printf '\nReady: bash demo/launch.sh\n'
