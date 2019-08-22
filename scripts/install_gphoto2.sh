#!/bin/bash

apt-get update && apt-get install -y wget \
&&  wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh -O /tmp/gphoto2-updater.sh \
&&  chmod +x /tmp/gphoto2-updater.sh \
&&  echo 2 | /tmp/gphoto2-updater.sh