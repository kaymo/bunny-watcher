#!/bin/bash

source ${HOME}/.bashrc
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
export LD_LIBRARY_PATH=/usr/local/lib

cd ${HOME}/bunny-watcher

rm -f upload_webcam.log upload_thermcam.log

# python ./animate.py webcam # |& cat > upload_webcam.log

for i in 2018-05-14 2018-05-15 2018-05-16 2018-05-17 2018-05-18 2018-05-19; do
    python ./animate.py thermcam "${i}" |& cat > "upload_thermcam_${i}.log"
done

cat upload_webcam.log
cat upload_thermcam.log

