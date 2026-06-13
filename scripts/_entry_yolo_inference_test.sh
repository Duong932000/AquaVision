#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

read -rp "Source (image/video/youtube): " SOURCE
read -rp "Model [runs/detect/train/weights/best.pt]: " MODEL

read -rp "Confidence [0.25]: " CONF

MODEL="${MODEL:-runs/detect/train/weights/best.pt}"
CONF="${CONF:-0.25}"

python "$REPO_ROOT/helpers/inference_test.py" --source "$SOURCE" --model "$MODEL" --conf "$CONF"
