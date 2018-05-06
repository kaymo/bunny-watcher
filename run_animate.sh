#!/bin/bash

source ${HOME}/.bashrc
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
export LD_LIBRARY_PATH=/usr/local/lib

cd ${HOME}/bunny-watcher

python ./animate.py webcam |& cat > upload_webcam.log

python ./animate.py thermcam |& cat > upload_thermcam.log

cat upload_webcam.log
cat upload_thermcam.log

