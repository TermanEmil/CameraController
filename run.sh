#!/usr/bin/env bash
set -e;

(cd ./src/infrastructure/django_framework/ && ./entrypoint.sh);
./src/infrastructure/django_framework/manage.py runserver 0.0.0.0:5000;