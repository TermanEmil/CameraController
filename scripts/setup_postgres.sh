#!/usr/bin/env bash
set -e;

echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections;

apt-get update && apt-get install -y \
    libpq-dev           \
    postgresql          \
    postgresql-contrib;

# Run as postgres user the rest of the setup
su -c `realpath ./setup_postgres_db.sh` - postgres;