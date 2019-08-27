#!/usr/bin/env bash

# Requirements:
#  inotify-tools
#
#
# [Optional] For emailing: the web app should be running: localhost:5000 should be accessible.


PATH_TO_WATCH='./Timelapses/'
PATH_TO_MOVE_FILES_TO='/Mounted/Cern/Timelapse/Software/Timelapses'

mkdir -p ${PATH_TO_WATCH};
mkdir -p ${PATH_TO_MOVE_FILES_TO};

inotifywait -r -m ${PATH_TO_WATCH} -e close_write -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'";
	
        { # try
            rsync -rvh --chmod=a+rw --perms ${PATH_TO_WATCH} ${PATH_TO_MOVE_FILES_TO} --remove-source-files;
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
                curl localhost:5000/scheduling/api/sync_failed_error_email_send;
            } || { # catch
                echo 'Failed to send email' >&2;
            }
        }
    done