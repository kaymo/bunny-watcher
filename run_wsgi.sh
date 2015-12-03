#!/bin/bash

env PATH=/home/pi/bunny-watcher/bunny-watcherenv/bin
chdir /home/pi/bunny-watcher
exec uwsgi --ini bunny-watcher.ini
