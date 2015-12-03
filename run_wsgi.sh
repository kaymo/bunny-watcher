#!/bin/bash

env PATH=/home/pi/bunny-watcher/bunny-watcherenv/bin
cd /home/pi/bunny-watcher
exec uwsgi --ini bunnies.ini
