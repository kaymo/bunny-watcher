#!/usr/bin/env python

# Dependencies: Flask
from flask import Flask, url_for, render_template, request
import os
import binascii

application = Flask(__name__)

# Create the app
application.config['DEBUG'] = False

def remove_items(full_list, to_remove):
    return [item for item in full_list if not item in to_remove]

# Index page
@application.route("/")
def show_capture():
    capture = request.args.get('capture')
    print capture

    # Get a list of the captures that doesn't include the current captures
    captures = sorted(os.listdir('static/captures/webcam/'), reverse=True)
    
    # Remove "current" and "animated" and "webcam"
    captures = remove_items(captures, ["current.jpg", "webcam.mp4", "animated.mp4"])

    # Remove the file extensions
    captures = [filename[:-4] for filename in captures]

    # Set the capture being shown as either the selected one, or the first available (without the file extension)
    if capture == None:
        capture = captures[0]

    videos = sorted(os.listdir('static/videos/'), reverse=True)

    return render_template('main.html', 
        capture_name=capture, captures=captures, videos=videos)


# Start the app and make available to all
if __name__ == "__main__":
    application.run(host='0.0.0.0')

# EOF
