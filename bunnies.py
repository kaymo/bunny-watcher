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

def get_capture_names(path):
    # Get a list of the captures
    captures = sorted_ls(path)

    # Remove the file extensions
    captures = [filename[:-4] for filename in captures]

    # Remove "current" and "animated" and "webcam"
    captures = remove_items(captures, ["current", "webcam", "animated", "thermcam"])

    return captures

# Index page
@application.route("/")
def show_capture():
    capture = request.args.get('capture')
    print capture

    # Get a list of the captures
    captures_web = get_capture_names('static/captures/webcam/')
    captures_therm = get_capture_names('static/captures/thermcam/')

    # Get the deduped joint list of captures
    captures = list(sorted(set(captures_web + captures_therm), reverse=True))

    # Set the capture being shown with either the selected one, or the first available (without the file extension)
    if capture == None:
        capture = captures[0]

    show_webcam = capture in captures_web
    show_thermcam = capture in captures_therm

    videos = sorted_ls('static/videos/')

    return render_template('main.html', 
        capture_name=capture, show_webcam=show_webcam, show_thermcam=show_thermcam,
        captures=captures, videos=videos)


# Start the app and make available to all
if __name__ == "__main__":
    application.run(host='0.0.0.0')

# EOF
