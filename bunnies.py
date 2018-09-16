#!/usr/bin/env python

# Dependencies: Flask
from flask import Flask, url_for, render_template, request, redirect
import os
import binascii
import numpy as np
import math

application = Flask(__name__)

# Create the app
application.config['DEBUG'] = False

def remove_items(full_list, to_remove):
    return [item for item in full_list if not item in to_remove]

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime, reverse=True))

def get_capture_names(path, limit=False):
    # Get a list of the captures
    captures = reversed(sorted(os.listdir(path)))

    # Remove the file extensions
    captures = [filename[:-4] for filename in captures]

    # Remove "current" and "animated" and "webcam"
    captures = remove_items(captures, ["current", "webcam", "animated", "thermcam"])

    limit = False

    if limit:
        image_count = len(captures)
        select_count = 300
        base = 10.0
        max_in_base = math.log(image_count, base)

        indexes = sorted(list(set([int(round(x)) for x in np.logspace(0, max_in_base, num=select_count, base=base)])))

        captures = [captures[idx-1] for idx in indexes]

    return captures

# Index page
@application.route("/")
def show_capture():
    capture = request.args.get('capture')

    # Get a list of the captures
    captures_web = get_capture_names('static/captures/webcam/')
    captures_therm = get_capture_names('static/captures/thermcam/', limit=True)

    # Get the deduped joint list of captures
    captures = list(sorted(set(captures_web + captures_therm), reverse=True))

    # Set the capture being shown with either the selected one, or the first available (without the file extension)
    if capture == None:
        capture = captures[0]

    show_webcam = capture in captures_web # if not capture else True
    show_thermcam = capture in captures_therm if not capture else True

    videos = sorted_ls('static/videos/')

    return render_template('main.html', 
        capture_name=capture, show_webcam=show_webcam, show_thermcam=show_thermcam,
        captures=captures, videos=videos)


def get_next_capture(capture, go_back):
    # Get a list of the captures
    captures_web = get_capture_names('static/captures/webcam/')
    captures_therm = get_capture_names('static/captures/thermcam/')

    # Get the deduped joint list of captures
    captures = list(sorted(set(captures_web + captures_therm), reverse=True))

    # Index of current capture
    try:
        index = captures.index(capture)
    except:
        return capture

    new_index = index - 1 if go_back else index + 1

    if new_index < 0 or new_index >= len(captures):
        return capture

    return captures[new_index]


# Navigate between captures using arrow left/right
@application.route("/next")
def next_capture():
    capture = request.args.get('capture')
    back = request.args.get('back')

    next_capture = get_next_capture(capture, back == '1')
    return redirect(url_for('show_capture', capture=next_capture))


# Start the app and make available to all
if __name__ == "__main__":
    application.run(host='0.0.0.0')

# EOF
