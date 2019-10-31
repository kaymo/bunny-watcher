desc="Pomona Watcher"
category="15"  
title="Pomona (test)"
file="test.webm"

python upload_video.py --noauth_local_webserver --file="${file}" --title="${title}" --description="${desc}" --category="${category}"

