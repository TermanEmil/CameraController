#!/usr/bin/env bash
set -e;

virtualenv .venv -p python3.7 \
&&  source .venv/bin/activate \
&&  pip install -r requirements.txt \
&&  pip install -e ./src/
