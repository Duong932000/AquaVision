#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -d ".venv" ]; then
    echo "[ERROR] .venv not found"
    echo "Run setup-venv.sh first"
    exit 1
fi

source .venv/bin/activate

echo ""
echo "========================================"
echo " AquaVision YOLO11 Model Downloader"
echo "========================================"
echo ""

MODELS_DIR="models/raw"

mkdir -p "$MODELS_DIR"

echo "Available YOLO11 models:"
echo ""
echo "  n  -> YOLO11 Nano"
echo "  s  -> YOLO11 Small"
echo "  m  -> YOLO11 Medium"
echo "  l  -> YOLO11 Large"
echo "  x  -> YOLO11 Extra Large"
echo ""

read -rp "Select model (n/s/m/l/x): " MODEL_TYPE

case "$MODEL_TYPE" in
    n) MODEL_NAME="yolo11n.pt" ;;
    s) MODEL_NAME="yolo11s.pt" ;;
    m) MODEL_NAME="yolo11m.pt" ;;
    l) MODEL_NAME="yolo11l.pt" ;;
    x) MODEL_NAME="yolo11x.pt" ;;
    *)
        echo "[ERROR] Invalid model selection"
        exit 1
        ;;
esac

echo ""
echo "[INFO] Selected model: $MODEL_NAME"

TARGET_PATH="$MODELS_DIR/$MODEL_NAME"

if [ -f "$TARGET_PATH" ]; then
    echo "[INFO] Model already exists:"
    echo "       $TARGET_PATH"
    exit 0
fi

echo ""
echo "[INFO] Downloading model..."

python - <<PYTHON
from ultralytics import YOLO

print("Downloading ${MODEL_NAME} ...")

YOLO("${MODEL_NAME}")

print("Download completed.")
PYTHON

if [ ! -f "$MODEL_NAME" ]; then
    echo "[ERROR] Download failed"
    exit 1
fi

mv "$MODEL_NAME" "$TARGET_PATH"

echo ""
echo "[INFO] Model saved to:"
echo "       $TARGET_PATH"

echo ""
echo "========================================"
echo " Download Completed"
echo "========================================"
echo ""