#!/bin/bash

sudo uvcdynctrl -s 'LED1 Mode' 0

cd /home/pi/bunny-watcher
# kernprof --line-by-line ./sense.py
python ./sense.py
