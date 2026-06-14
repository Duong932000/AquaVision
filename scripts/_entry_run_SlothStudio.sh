#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

export ROOT_DIR="$REPO_ROOT"
echo "ROOT_DIR=$ROOT_DIR"

python "$REPO_ROOT/SlothStudio/SlothStudio.py"
