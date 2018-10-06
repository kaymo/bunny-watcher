#!/bin/bash

source ${HOME}/.bashrc
export PATH=/usr/lib64/qt-3.3/bin:/usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/avj/.local/bin:/home/avj/bin
export LD_LIBRARY_PATH=/usr/local/lib

cd ${HOME}/bunny-watcher/animation

rm -f animate.log

./run.sh |& cat > animate.log

cat animate.log

# EOF
