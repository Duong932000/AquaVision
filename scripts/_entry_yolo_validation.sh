#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

echo "========================================"
echo " AquaVision YOLO26 Validator"
echo "========================================"

# parser user input
read -rp "Best.pt model path, e,g: runs/detect/train/weights/best.pt: " MODEL
read -rp "Data yaml path, e.g: data/aquavision.yaml: " DATA

echo "========================================"
echo " Validate Configuration"
echo "========================================"
echo "Dataset : ${DATA}"
echo "Model   : ${MODEL}"
echo "========================================"

yolo task=detect mode=val model="${MODEL}" data="${DATA}"
