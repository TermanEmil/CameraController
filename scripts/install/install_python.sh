#!/usr/bin/env bash

apt-get update;

apt-get install -y 				\
	software-properties-common	\
	python3.9					\
	python3.9-gdbm				\
	python3.9-dev				\
	python3.9-tk				\
	virtualenv;

# This is required for ubuntu and doesn't work for raspberry
add-apt-repository -y ppa:deadsnakes/ppa || echo 'Failed to add ppa:deadsnakes/ppa --- Skipping' >&2;

# Required for raspberry
apt-get -y install python3-gdbm || echo 'Failed to install python3-gdbm --- Skipping' >&2;

