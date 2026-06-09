#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

python $REPO_ROOT/examples/download_pothole_roboflow_dataset.py
