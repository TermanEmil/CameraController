#!/bin/bash

apt-get update && apt-get install -y git libusb-1.0-0 libusb-1.0-0-dev \
&&  git clone 'https://github.com/Yepkit/ykush.git' /tmpl/ykush \
&&  cd /tmpl/ykush \
&&  git reset --hard '4fab0ba2c1d9e610f11f8ae81739e897ee9e675e' \
&&  ./build.sh \
&&  cp -f bin/ykushcmd /usr/bin