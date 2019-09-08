#!/usr/bin/env bash

# Requirements:
#  inotify-tools
#
# ./scripts/mount_tools.sh
# [Optional] For emailing: the web app should be running: localhost:80 should be accessible.

# Exit on signal
trap "exit" SIGHUP SIGINT SIGTERM

. ./scripts/mount_tools.sh

PATH_TO_MOVE_FILES_TO="${MOUNT_POINT}/${TIMELAPSE_DEST}"

function sync_files() {
    SOURCE_DIR=$1
    DEST_DIR=$2
    VERBOSE_PREFIX=$3

    # rsync:
    #  --chmod: in case this is run as root:
    #   give everyone read & write permissions
    #  -i: print the copied files in the following format: >f+++++++++ my_file
    # grep:
    #  Extract only the lines that start with '>f' (to avoid dirs: '>d')
    # sed:
    #  Add a prefix to the copied file
    rsync \
        -ri \
        --chmod=a+rw --perms \
        ${SOURCE_DIR} ${DEST_DIR} \
        --remove-source-files \
        --prune-empty-dirs | \
    grep '^>f' | \
    sed "s/>f......... \(.*\)/${VERBOSE_PREFIX}\1/g"
}

function continously_try_to_mount() {
    while :
    do
        # Check if it's mounted.
        if is_mounted; then
            # It's mounted
            break
        else
            { # try to mount
                # There's a chance for files to sneak into the unmounted
                #  mount point. So, first, move those files to the timelapse dir
                # This happens when the mounted server is disconnected and
                #  files are still being transported or smth
                mkdir -p ${MOUNT_POINT};
                sync_files "${PATH_TO_MOVE_FILES_TO}/" ${TIMELAPSE_DIR} '[recovered]';

                do_the_mounting;
            } || { # catch
                echo '[error] Failed to mount' >&2;
            }
            sleep 1;
        fi
    done
}


mkdir -p ${TIMELAPSE_DIR}
inotifywait -r -m ${TIMELAPSE_DIR} -e close_write -e moved_to |
while read path action file; do
    # Continously try to move the files to the mounted server
    while :
    do
        continously_try_to_mount
        { # try
            mkdir -p ${PATH_TO_MOVE_FILES_TO};
            sync_files "${TIMELAPSE_DIR}/" ${PATH_TO_MOVE_FILES_TO} '[copied]';
            break;
        } || { # catch
            echo "[error] Failed to sync folders" >&2;
        }

        sleep 1
    done
done