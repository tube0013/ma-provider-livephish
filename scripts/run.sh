#!/bin/sh
# Start a Music Assistant server in dev mode that loads the provider from this repository.
# Its settings and library stay in .data; delete that folder to start over.
set -eu
cd "$(dirname "$0")/.."
PYTHONDEVMODE=1 exec .venv/bin/python -m music_assistant \
    --data-dir .data --cache-dir .data/.cache --dev-providers-dir . --log-level info "$@"
