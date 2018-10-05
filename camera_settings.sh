#!/bin/bash

# 
# uvcdynctrl -i /usr/share/uvcdynctrl/data/046d/logitech.xml |& cat > /dev/null
# uvcdynctrl --set='Focus, Auto' 0
# uvcdynctrl -s 'LED1 Mode' 0
# sudo v4l2-ctl -d /dev/video0 -c led1_mode=0
# sudo v4l2-ctl -d /dev/video0 -c focus_auto=0
# sudo v4l2-ctl -d /dev/video0 -c focus_absolute=0
# 

device=$(grep -l "Life" /sys/class/video4linux/*/name  | sort | head -n 1 | cut -d '/' -f 5)

#
# Need this twice
#
# v4l2-ctl -d /dev/${device} --set-ctrl=exposure_absolute=20
# v4l2-ctl -d /dev/${device} --set-ctrl=exposure_absolute=20
v4l2-ctl -d /dev/${device} --set-ctrl=exposure_auto=1
v4l2-ctl -d /dev/${device} --set-ctrl=backlight_compensation=10
v4l2-ctl -d /dev/${device} --set-ctrl=contrast=0
v4l2-ctl -d /dev/${device} --set-ctrl=sharpness=50

# EOF
