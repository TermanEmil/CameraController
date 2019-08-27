#!/usr/bin/env bash

set -e;

apt-get update && apt-get install -y \
    nfs-common \
    inotify-tools

./scripts/mount_nfs.sh