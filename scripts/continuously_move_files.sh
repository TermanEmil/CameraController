#!/usr/bin/env bash

# Requirements:
#  inotify-tools


PATH_TO_WATCH='./Timelapses/'
PATH_TO_MOVE_FILES_TO='/Mounted/Cern/Timelapse/Software/'


inotifywait -m ${PATH_TO_WATCH} -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
    done