#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR

./camera_settings.sh

# cd /home/pi/bunny-watcher
# export LD_LIBRARY_PATH=$(pwd):${LD_LIBRARY_PATH}
# export PYTHONPATH=/opt/ocv/lib/python2.7/dist-packages
export LD_LIBRARY_PATH=/opt/opencv/lib:/opt/libvpx/lib:/opt/libwebp/lib:/opt/ffmpeg/lib:/opt/libuvc/lib
export PYTHONPATH=/opt/opencv/lib/python3.8/dist-packages
export PYTHONPATH=${HOME}/purethermal1-uvc-capture/python:$PYTHONPATH
# kernprof --line-by-line ./sense.py
while true; do echo "STARTING"; nice -n -20 python3 -u ./sense.py; sleep 2; done

# EOF
