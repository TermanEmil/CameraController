#!/usr/bin/env bash
set -e;

apt-get install python3-dev
./scripts/install/install_python.sh
./scripts/install/install_gphoto2.sh

virtualenv .venv -p python3.7 \
&&  source .venv/bin/activate \
&&  pip install -r requirements.txt \
&&  pip install -e ./src/
