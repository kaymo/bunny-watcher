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

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime, reverse=True))

# Index page
@application.route("/")
def show_capture():
    capture = request.args.get('capture')
    print capture

    # Get a list of the captures that doesn't include the current captures
    captures = sorted_ls('static/captures/webcam/')

    # Remove the file extensions
    captures = [filename[:-4] for filename in captures]
    
    # Remove "current" and "animated" and "webcam"
    captures = remove_items(captures, ["current", "webcam", "animated"])

    # Set the capture being shown with either the selected one, or the first available (without the file extension)
    if capture == None:
        capture = captures[0]

    videos = sorted_ls('static/videos/')

    return render_template('main.html', 
        capture_name=capture, captures=captures, videos=videos)


# Start the app and make available to all
if __name__ == "__main__":
    application.run(host='0.0.0.0')

# EOF
