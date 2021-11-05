#!/usr/bin/env bash
set -e;

echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections;

apt-get update && apt-get install -y \
    libpq-dev           \
    postgresql          \
    postgresql-contrib;

service postgresql@12-main restart;

