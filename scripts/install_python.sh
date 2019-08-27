#!/usr/bin/env bash

apt-get update && apt-get -y install software-properties-common \
&&  add-apt-repository -y ppa:deadsnakes/ppa \
&&  apt-get install python3.7
