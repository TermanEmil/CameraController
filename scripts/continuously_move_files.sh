#!/usr/bin/env bash

# Requirements:
#  inotify-tools


PATH_TO_WATCH='./Timelapses/'
PATH_TO_MOVE_FILES_TO='/Mounted/Cern/Timelapse/Software/Timelapses'

inotifywait -r -m ${PATH_TO_WATCH} -e close_write -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'";
	
	{ # try
	    rsync -rvh ${PATH_TO_WATCH} ${PATH_TO_MOVE_FILES_TO} --remove-source-files;
	} || { # catch
	    echo 'Failed to sync folders' >&2;
	    echo 'Trying to mount...';
	
	    { # try
	    	./scripts/mount_nfs.sh;
	    } || { # catch
		echo 'Failed to mount' >&2;
	    }
	}
    done
