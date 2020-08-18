#!/usr/bin/env bash

apt-get update\
&&  apt-get -y install software-properties-common \
&&  apt-get install -y python3.7;

apt get install -y virtualenv python3.7-dev python3-tk;

# This is required for ubuntu and doesn't work for raspberry
add-apt-repository -y ppa:deadsnakes/ppa || echo 'Failed to add ppa:deadsnakes/ppa --- Skipping' >&2;

# Required for raspberry
apt-get -y install python3-gdbm || echo 'Failed to install python3-gdbm --- Skipping' >&2;

