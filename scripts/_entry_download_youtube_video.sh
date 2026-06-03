#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

read -rp "YouTube URL: " URL
read -rp "Fish type (tilapia, catfish, etc.): " FISH_TYPE
read -rp "Start time, e.g: 01:45 " START_TIME
read -rp "Duration (seconds) [300]: " DURATION

DURATION="${DURATION:-300}"

python $REPO_ROOT/helpers/download_youtube_video.py --url "$URL" --fish-type "$FISH_TYPE" --start-time "$START_TIME" --duration "$DURATION"
