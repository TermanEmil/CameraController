#!/usr/bin/env bash

# A command to quickly share the code.
rsync -avz --exclude './.git' --filter=':- .gitignore' ./ eterman@nucpcaps1:/home/Projects/Timelapse