#!/usr/bin/env bash

set -euxo pipefail

cd "$(dirname "$0")"

echo "========================================"
echo " AquaVision Development Environment"
echo "========================================"

# Verify project files
if [ ! -f "pyproject.toml" ]; then
    echo "[ERROR] pyproject.toml not found"
    exit 1
fi

# Detect Package Manager
if command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
elif command -v apt >/dev/null 2>&1; then
    PKG_MANAGER="apt"
else
    echo "[ERROR] Unsupported package manager"
    exit 1
fi

echo "[INFO] Package manager: $PKG_MANAGER"

# Install uv
if ! command -v uv >/dev/null 2>&1; then
    echo "[INFO] Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv >/dev/null 2>&1; then
        echo "[ERROR] Failed to install uv"
        exit 1
    fi
fi

echo "[INFO] uv version: $(uv --version)"

# Install Python 3.11
if ! command -v python3.11 >/dev/null 2>&1; then
    echo "[INFO] Installing Python 3.11..."
    if [ "$PKG_MANAGER" = "dnf" ]; then
        sudo dnf install -y \
            python3.11 \
            python3.11-devel \
            python3-tkinter \
            gcc \
            gcc-c++ \
            make \
            git \
            tk \
            tk-devel \
            tcl \
            tcl-devel
    else
        sudo apt update
        sudo apt install -y \
            python3.11 \
            python3.11-venv \
            python3.11-dev \
            python3-tk \
            build-essential \
            git \
            tk-dev \
            tcl-dev
    fi
fi

echo "[INFO] Python version:"
python3.11 --version

# Remove broken venv if requested
if [ "${1:-}" = "--clean" ]; then
    echo "[INFO] Removing existing virtual environment..."
    rm -rf .venv
fi

# Create Virtual Environment
if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment..."
    uv venv .venv --python 3.11
else
    echo "[INFO] Existing .venv detected"
fi

# Sync dependencies from pyproject.toml
echo "[INFO] Installing AquaVision dependencies..."

uv sync --extra dev  --extra api --extra ml

# Verify environment
echo "[INFO] Installed packages:"
uv pip list
echo "[INFO] Python executable:"
uv run which python
echo "[INFO] Python version inside venv:"

uv run python --version

echo "========================================"
echo " Setup Completed Successfully"
echo "========================================"
