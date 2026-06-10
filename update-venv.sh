#!/usr/bin/env bash

source .venv/bin/activate

uv pip install -e ".[dev,api,dashboard,ml]" --upgrade
