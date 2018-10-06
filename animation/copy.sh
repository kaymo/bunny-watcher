#!/bin/bash

set -e
set -u
set -v
set -x

mkdir empty_dir
rsync -a --delete empty_dir thermcam
rsync -a --delete empty_dir webcam
rm -rf thermcam webcam empty_dir
mkdir thermcam webcam

web=$(ls -tr ~/bunny-watcher/static/captures/webcam/*.webp | tail -n 1)
base=$(basename $web)
base="*.webp"

rsync --info=progress2 -aHXxv --numeric-ids --delete --progress -e "ssh -T -c arcfour -o Compression=no -x" ~/bunny-watcher/static/captures/thermcam/${base} thermcam

rsync --info=progress2 -aHXxv --numeric-ids --delete --progress -e "ssh -T -c arcfour -o Compression=no -x" ~/bunny-watcher/static/captures/webcam/${base} webcam

# EOF

