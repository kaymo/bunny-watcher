#!/usr/bin/env python

# Dependencies: Flask
from flask import Flask, url_for, render_template
import os

application = Flask(__name__)

# Create the app
#app = Flask('sybil')
application.config['DEBUG'] = False

# Index page


@application.route("/")
def show_capture():

    # Get a list of the captures that doesn't include the current captures
    images = sorted(os.listdir('static/captures/'), reverse=True)
    images = images[4:]

    videos = sorted(os.listdir('static/videos/'), reverse=True)
    videos = videos

    return render_template('main.html', images=images, videos=videos)

# Start the app and make available to all
if __name__ == "__main__":
    application.run(host='0.0.0.0')

# EOF
