#!/usr/bin/env bash

# This scripts mounts the nfs server, unless it's already mounted.

# Requirements:
#  nfs-common

# unmount - to unmount


function is_mounted() {
    if [[ $(mount -v | grep ${MOUNT_POINT}) ]]; then
        return 0; # true
    else
        return 1; # false
    fi
}


function do_the_mounting() {
    mkdir -p ${MOUNT_POINT}

    if ! is_mounted; then
        mount ${MOUNT_REMOTE_NODE} ${MOUNT_POINT};
    fi
}