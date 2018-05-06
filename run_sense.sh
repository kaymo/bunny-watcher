#!/bin/bash

sudo uvcdynctrl -i /usr/share/uvcdynctrl/data/046d/logitech.xml |& cat > /dev/null
sudo uvcdynctrl --set='Focus, Auto' 1
sudo uvcdynctrl -s 'LED1 Mode' 0 |& cat > /dev/null

cd /home/pi/bunny-watcher
export LD_LIBRARY_PATH=$(pwd):${LD_LIBRARY_PATH}
# kernprof --line-by-line ./sense.py
python ./sense.py
