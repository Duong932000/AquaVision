#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

read -rp "Fish Type [koi]: " FISH_TYPE
read -rp "Frames per Video [15]: " FRAMES_PER_VIDEO
read -rp "Dataset Version [1]: " VERSION

FISH_TYPE="${FISH_TYPE:-koi}"
FRAMES_PER_VIDEO="${FRAMES_PER_VIDEO:-15}"
VERSION="${VERSION:-1}"

python "$REPO_ROOT/helpers/process_raw_dataset.py" --fish-type "$FISH_TYPE" --frames-per-video "$FRAMES_PER_VIDEO" --version "$VERSION"

echo "[INFO] Dataset generated:"
echo "datasets/${FISH_TYPE}/processed/dataset.${FISH_TYPE}.v${VERSION}"
