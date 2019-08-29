#!/usr/bin/env bash

# Requirements:
#  inotify-tools
#
# ./scripts/mount_nfs.sh
# [Optional] For emailing: the web app should be running: localhost:80 should be accessible.


PATH_TO_WATCH='./Timelapses/'
PATH_TO_MOVE_FILES_TO='/Mounted/Cern/Timelapse/Software/Timelapses'

mkdir -p ${PATH_TO_WATCH};
mkdir -p ${PATH_TO_MOVE_FILES_TO};

inotifywait -r -m ${PATH_TO_WATCH} -e close_write -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'";

        # Continuously try to mount the nfs server
        while :
        do
            # Check if NFS server is mounted.
            if [[ $(mount -v | grep Mounted/Cern) ]]; then
                # It's mounted
                break
            else
                { # try to mount it
                    ./scripts/mount_nfs.sh;
                } || { # catch
                    echo 'Failed to mount nfs server'
                }
                sleep 1;
            fi
        done

        # Move the files to the nfs server
        { # try
            # chmod: in case this is run as root, give everyone read & write permissions
            rsync -rvh --chmod=a+rw --perms ${PATH_TO_WATCH} ${PATH_TO_MOVE_FILES_TO} --remove-source-files --prune-empty-dirs;
        } || { # catch
            echo 'Failed to sync folders' >&2;
            echo 'Trying to (re)mount...';

            { # try
                ./scripts/mount_nfs.sh;
            } || { # catch
                echo 'Failed to mount' >&2;
            };

            echo 'Trying to send an email about this accident...';
            { # try
                curl localhost/scheduling/api/sync_failed_error_email_send;
            } || { # catch
                echo 'Failed to send email' >&2;
            }
        }
    done