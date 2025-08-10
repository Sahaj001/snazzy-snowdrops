#!/bin/bash
set -e

# Default port (override with: PORT=9000 ./scripts/serve.sh)
PORT=${PORT:-8000}

echo "Starting Snazzy Snowdrops dev server on http://localhost:${PORT}"

# Use Poetry if available, otherwise fallback to system Python
if command -v poetry &>/dev/null; then
    poetry run python src/main.py "$PORT"
elif command -v python3 &>/dev/null; then
    echo "Poetry not found. Using default system Python"
    python3 src/main.py "$PORT"
else
    echo "Error: No Python found. Install Python 3.10+ or Poetry."
    exit 1
fi
