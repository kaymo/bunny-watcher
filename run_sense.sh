#!/bin/bash

# 
uvcdynctrl -i /usr/share/uvcdynctrl/data/046d/logitech.xml |& cat > /dev/null
uvcdynctrl --set='Focus, Auto' 0
uvcdynctrl -s 'LED1 Mode' 0
# sudo v4l2-ctl -d /dev/video0 -c led1_mode=0
# sudo v4l2-ctl -d /dev/video0 -c focus_auto=0
# sudo v4l2-ctl -d /dev/video0 -c focus_absolute=0
# 

# cd /home/pi/bunny-watcher
export LD_LIBRARY_PATH=$(pwd):${LD_LIBRARY_PATH}
# kernprof --line-by-line ./sense.py
while true; do echo "STARTING"; python ./sense.py; sleep 2; done

