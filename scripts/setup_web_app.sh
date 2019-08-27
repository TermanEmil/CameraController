#!/usr/bin/env bash
set -e;

apt-get update && apt-get install -y virtualenv

./scripts/install_python.sh
./scripts/install_gphoto2.sh
./scripts/install_ykush.sh

virtualenv .venv -p python 3.7 \
&&  source .venv/bin/activate \
&&  pip install -r requirements.txt