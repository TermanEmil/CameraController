#!/usr/bin/env bash

# Installs
apt-get update && apt-get install -y \
    nfs-common \
    inotify-tools

./scripts/install_python.sh
./scripts/install_gphoto2.sh
./scripts/install_ykush.sh


# Other
./scripts/mount_nfs.sh
