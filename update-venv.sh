#!/usr/bin/env bash

source .venv/bin/activate

uv pip install -e ".[dev,api,database,ml]" --upgrade
