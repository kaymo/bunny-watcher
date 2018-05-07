#!/usr/bin/env python

# Dependencies: Flask
from flask import Flask, url_for, render_template
import os
import binascii

application = Flask(__name__)

# Create the app
#app = Flask('sybil')
application.config['DEBUG'] = False

# Index page

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime, reverse=True))

@application.route("/")
def show_capture():

    # Get a list of the captures that doesn't include the current captures
    images = sorted_ls('static/captures/webcam/')
    # remove "current" and "animated"
    try:
        images.remove("current.jpg")
    except:
        pass

    try:
        images.remove("animated.mp4")
    except:
        pass
    # and now remove whatever is currently showing!
    current = images[0]
    images = images[1:]

    videos = sorted_ls('static/videos/')

    return render_template(
        'main.html', w_current="current.jpg", t_current="current.png",
        images=images, videos=videos,
        rand=int(binascii.hexlify(os.urandom(8)),
                 16))


# Start the app and make available to all
if __name__ == "__main__":
    application.run(host='0.0.0.0')

# EOF
