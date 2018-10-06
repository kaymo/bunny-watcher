#!/bin/bash

set -x
set -u
set -e
set -v

./copy.sh

export MAGICK_THREAD_LIMIT=1
nice -n 20 python -u ./animate.py

# EOF
