#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

echo "Activating virtual environment..."
source .venv/bin/activate

echo "========================================"
echo " AquaVision YOLO26 Trainer"
echo "========================================"

# parser user input
read -rp "Dataset YAML [datasets/koi/datasets/Koi.v1-koi.dataset.194.images.13062026.yolo26/data.yaml]: " DATASET_YAML
read -rp "Model [yolo26n.pt]: " MODEL
read -rp "Epochs [100]: " EPOCHS
read -rp "Image Size [512, 1280]: " IMGSZ

MODEL="${MODEL:-yolo26n.pt}"
EPOCHS="${EPOCHS:-100}"
IMGSZ="${IMGSZ:-512}"

echo "========================================"
echo " Training Configuration"
echo "========================================"
echo "Dataset : ${DATASET_YAML}"
echo "Model   : ${MODEL}"
echo "Epochs  : ${EPOCHS}"
echo "Imgsz   : ${IMGSZ}"
echo "========================================"
echo

yolo task=detect mode=train data="${DATASET_YAML}" model="${MODEL}" epochs="${EPOCHS}" imgsz="${IMGSZ}"

echo "[INFO] Training completed."
echo "[INFO] Check results under:"
echo "runs/detect/"
