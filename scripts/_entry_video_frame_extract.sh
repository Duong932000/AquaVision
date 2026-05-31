#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

read -rp "Video path [1]: " VIDEO_PATH
read -rp "Extract FPS [2]: " FPS

FPS="${FPS:-1}"

python $REPO_ROOT/helpers/extract_frames.py --video-path "$VIDEO_PATH" --fps "$FPS"

echo "[INFO] Frames saved to:"
echo "datasets/frames"
