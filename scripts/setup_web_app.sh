#!/usr/bin/env bash
set -e;

./scripts/install_python.sh
./scripts/install_gphoto2.sh
./scripts/install_ykush.sh || echo 'Failed to install ykush --- Ignoring' >&2

apt-get update && apt-get install -y virtualenv python3.7-dev python3-tk

virtualenv .venv -p python3.7 \
&&  source .venv/bin/activate \
&&  pip install -r requirements.txt \
&&  pip install -e ./src/