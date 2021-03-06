#!/usr/bin/env python

import os
import datetime
import shutil
import sys

CAMERA = sys.argv[1]

BUNNY_WATCHER_DIR = os.path.expandvars("${HOME}/bunny-watcher")
CAPTURES_DIR = os.path.join(BUNNY_WATCHER_DIR, "static/captures", CAMERA)
VIDEOS_DIR = os.path.join(BUNNY_WATCHER_DIR, "static/videos")

ext_map = {}
ext_map["webcam"] = "jpg"
ext_map["thermcam"] = "png"

if not os.path.exists(VIDEOS_DIR):
    os.makedirs(VIDEOS_DIR)

try:

    # Create .gif for Bunny Watcher
    # os.system("ffmpeg -y -framerate 10 -pattern_type glob -i '{}/2*.jpg' -pix_fmt rgb8 -ignore_loop 0 -s 576x384 {}/animated.gif".format(CAPTURES_DIR, CAPTURES_DIR) )

    # Create .mp4 for YouTube
    framerate = 20
    quality = 2

    filename = "{:s}.mp4".format(CAMERA)

    """
    Kim's command
    """
    ffmpeg_command = "ffmpeg -y -pattern_type glob -i '{input:s}/2*.{ext:s}' -framerate {framerate:d} -vcodec mpeg4 -q:v {quality:d} {output:s}/{filename:s}"
    """
    Andrew's commands
    """
    # ffmpeg_command = "ffmpeg -y -pattern_type glob -i '{input:s}/2*.jpg' -framerate {framerate:d} -vcodec libx264 -crf 25 -preset medium -pix_fmt yuv420p {output:s}/animated.mp4"
    # ffmpeg_command = "ffmpeg -y -pattern_type glob -i '{input:s}/2*.jpg' -framerate {framerate:d} -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 28 {output:s}/animated.mp4"
    # ffmpeg_command = "ffmpeg -y -pattern_type glob -i '{input:s}/2*.jpg' -framerate {framerate:d} -c:v libx264 -flags:v '+cgop' -g 15 -bf 1 -coder ac -profile:v high -crf 21 -pix_fmt yuv420p -movflags faststart {output:s}/animated.mp4"

    ffmpeg_command = ffmpeg_command.format(
        input=CAPTURES_DIR, ext=ext_map[CAMERA],
        framerate=framerate, quality=quality, output=CAPTURES_DIR,
        filename=filename)

    print ffmpeg_command

    os.system(ffmpeg_command)

    # Copy the mp4 to the back-up location
    curr_time = datetime.datetime.now().isoformat().replace(".", "_").replace(":", "_")
    curr_mp4_path = os.path.join(VIDEOS_DIR, curr_time + ".mp4")
    shutil.copyfile(os.path.join(CAPTURES_DIR, filename), curr_mp4_path)

    # YouTube details
    desc = "Bunny Watcher ({:s})".format(CAMERA)
    category = "15"   # Pets & Animals YouTube category ID
    # Changing this to today's date as we're now uploading at 23:00!
    # title = (datetime.date.today() - datetime.timedelta(1)
    #         ).strftime('%A %-e %B %Y')  # Yesterday's date
    title = "Bunnies ({:s}) - {}".format(CAMERA,
                                         datetime.date.today().strftime('%A %-e %B %Y'))

    # Upload to YouTube
    # os.system("python {}/upload_video.py --noauth_local_webserver --file='{}/{}' --title='{}' --description='{}' --category={}".format(
    #    BUNNY_WATCHER_DIR, CAPTURES_DIR, filename, title, desc, category))

except KeyboardInterrupt:
    print "Quitting ..."

# EOF
