#!/usr/bin/env bash

# Requirements:
#  inotify-tools
#
# ./scripts/mount_tools.sh

# Exit on signal
trap 'kill $(jobs -p) 2>&- || true' EXIT

. ./scripts/mount_tools.sh
. ./scripts/appsettings.sh

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
    { # try
      rsync \
          -ri \
          --chmod=a+rw --perms \
          "${SOURCE_DIR}" "${DEST_DIR}" \
          --remove-source-files \
          --prune-empty-dirs | \
      grep '^>f' | \
      sed "s/>f......... \(.*\)/${VERBOSE_PREFIX}\1/g"
    } || { # catch
      echo 'rsync failed. --- ignoring' >&2;
    }
}

function continously_try_to_mount() {
  while :
  do
    if is_mounted; then
      break
    else
      { # try
        # There's a chance for files to sneak into the unmounted
        #  mount point. So, first, move those files to the timelapse dir
        # This happens when the mounted server is disconnected and
        #  files are still being transported or smth
        mkdir -p ${MOUNT_POINT};

        # If the directory exists
        if [ -d "${PATH_TO_MOVE_FILES_TO}" ]; then
          sync_files "${PATH_TO_MOVE_FILES_TO}/" "${TIMELAPSE_DIR}" '[recovered]';
        fi
      } || { # catch
        echo '[error] Failed to recover unstransferred files' >&2;
      }

      { # try
        do_the_mounting;
      } || { # catch
        echo '[error] Failed to mount' >&2;
      }
      sleep 1;
    fi
  done
}


function sync_core() {
  inotifywait -r -m "${TIMELAPSE_DIR}" -e close_write -e moved_to |
    while read path action file; do
      # Continously try to move the files to the mounted server
      while :
      do
        continously_try_to_mount
        { # try
          mkdir -p "${PATH_TO_MOVE_FILES_TO}";
          sync_files "${TIMELAPSE_DIR}/" "${PATH_TO_MOVE_FILES_TO}" '[copied]';
          break;
        } || { # catch
          echo "[error] Failed to sync folders" >&2;
        }

        sleep 1;
      done
    done
}


# If inotifywait is not available - exit
if ! type inotifywait 2>&-; then
  echo 'inotifywait - not found' >&2;
  exit 1;
fi;

mkdir -p "${TIMELAPSE_DIR}"


while :
do
  { # try
    sync_core
  } || { # catch
    echo '[error] Inotify crashed --- Restarting' >&2;
  }

  sleep 1;
done
