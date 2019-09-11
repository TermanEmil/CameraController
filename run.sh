#!/usr/bin/env bash

set -e;

# Exit on signal
trap 'kill $(jobs -p) || true' EXIT

while :
do
  # Kill all the process using port 5000
  (lsof -ti tcp:5000 | xargs kill -2 2>&-) || true;
  pkill -f run_timelapse_file_transfer.sh || true;

  # Read configs vars
  set -a && . ./scripts/configs.sh && set +a;

  { # try
    (cd ./src/infrastructure/django_framework/ && ./entrypoint.sh);
    ./src/infrastructure/django_framework/manage.py runserver 0.0.0.0:5000;
  } || { # catch
    echo '[Error] Crashed or smth. Restarting' >&2;
  }
done