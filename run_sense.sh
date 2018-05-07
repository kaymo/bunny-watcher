#!/bin/bash

sudo uvcdynctrl -i /usr/share/uvcdynctrl/data/046d/logitech.xml |& cat > /dev/null
sudo uvcdynctrl --set='Focus, Auto' 0
sudo uvcdynctrl -s 'LED1 Mode' 0
sudo v4l2-ctl -d /dev/video0 -c led1_mode=0
sudo v4l2-ctl -d /dev/video0 -c focus_auto=0
sudo v4l2-ctl -d /dev/video0 -c focus_absolute=0

cd /home/pi/bunny-watcher
export LD_LIBRARY_PATH=$(pwd):${LD_LIBRARY_PATH}
# kernprof --line-by-line ./sense.py
python ./sense.py
