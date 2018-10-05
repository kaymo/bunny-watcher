#!/bin/bash

./camera_settings.sh

# cd /home/pi/bunny-watcher
export LD_LIBRARY_PATH=$(pwd):${LD_LIBRARY_PATH}
# kernprof --line-by-line ./sense.py
while true; do echo "STARTING"; python -u ./sense.py; sleep 2; done

