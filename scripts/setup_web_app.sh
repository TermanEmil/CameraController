#!/usr/bin/env bash
set -e;

./scripts/install/install_python.sh
./scripts/install/install_gphoto2.sh
./scripts/install/install_ykush.sh || echo 'Failed to install ykush --- Ignoring' >&2

virtualenv .venv -p python3.7 \
&&  source .venv/bin/activate \
&&  pip install -r requirements.txt \
&&  pip install -e ./src/
