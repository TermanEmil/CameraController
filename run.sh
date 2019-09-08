#!/usr/bin/env bash

set -e;

# Exit on signal
trap "exit" SIGHUP SIGINT SIGTERM

set -a && . ./scripts/configs.sh && set +a;

(cd ./src/infrastructure/django_framework/ && ./entrypoint.sh);
./src/infrastructure/django_framework/manage.py runserver 0.0.0.0:80;