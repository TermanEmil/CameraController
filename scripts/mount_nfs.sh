#!/usr/bin/env bash

DEVICE='128.141.50.125:aps'
DIR_TO_MOUNT='/Mounted/Cern/'

mkdir -p $DIR_TO_MOUNT
mount $DEVICE $DIR_TO_MOUNT
