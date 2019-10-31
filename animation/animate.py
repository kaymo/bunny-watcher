#!/usr/bin/env python

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

try:
    from builtins import int
except ImportError:
    pass

try:
    from future_builtins import *
except ImportError:
    pass

try:
    input = raw_input
except NameError:
    pass

try:
    range = xrange
except NameError:
    pass

import glob
import os
import subprocess
import shlex
import shutil
import multiprocessing
import datetime


def process_frame(args):
    """
    Handler that gets called subprocess to process the frames
    """
    webcam, thermcam, output, height, quality = args
    resize_image(webcam, height, quality)
    merge_frames(webcam, thermcam, output, quality)


def resize_image(image, height, quality):
    """
    Resizes a given image to a certain height
    """
    cmd = shlex.split("convert -resize x{height:s} {image:s} -quality {quality:d} {image:s}".format(
        height=height, image=image, quality=quality))
    out = subprocess.check_output(cmd)


def merge_frames(image1, image2, output, quality):
    """
    Creates the montage of the two frames
    """
    cmd = shlex.split(
        "montage {image1:s} {image2:s} -tile 2x1 -geometry +0+0 -quality {quality:d} {output:s}".
        format(image1=image1, image2=image2, quality=quality, output=output))
    out = subprocess.check_output(cmd)


class MontageVideo(object):
    """
    Class to generate the video from two directories
    """

    def __init__(self):
        self.webcam_path = "webcam"
        self.thermcam_path = "thermcam"
        self.montage_path = "montage"

        time_now = datetime.datetime.now()
        fdate = time_now.isoformat().replace(".", "_").replace(":", "_")
        self.output_name = "{date:s}.webm".format(date=fdate)

        #
        # Common files
        #
        self.common = None

        #
        # Quality
        #
        self.quality = 90

        ffmpeg_dir = "/usr/local/bin" # "ffmpeg-git-20181002-64bit-static"
        self.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg")
        self.ffprobe = os.path.join(ffmpeg_dir, "ffprobe")

        #
        # Limit the number of threads
        #
        self.threads = 3

    def cleanup(self):
        #
        # Clean-up the montage folder
        #
        if os.path.exists(self.montage_path):
            shutil.rmtree(self.montage_path)
        os.makedirs(self.montage_path)

    def find_common_files(self):
        #
        # Find all of the common files between the two directories
        #
        webcam = set(
            [os.path.basename(image)
             for image in glob.glob(
                 os.path.join(self.webcam_path, "*.webp"))])
        thermcam = set(
            [os.path.basename(image)
             for image in glob.glob(
                 os.path.join(self.thermcam_path, "*.webp"))])
        # self.common = thermcam.intersection(webcam)

        # Hack -- only process therm
        self.common = thermcam

    def find_height(self):
        #
        # Find the height of the thermcam images dynamically
        #
        random_image = os.path.join(
            self.thermcam_path, next(iter(self.common)))
        cmd = shlex.split("identify {:s}".format(random_image))
        out = subprocess.check_output(cmd)
        dimensions = out.strip().split()[2]
        self.height = dimensions.split("x")[1]
        print(self.height)

    def process_frames(self):
        #
        # Iterates over all the frames using multiprocessing
        #
        all_frames = []

        for frame in self.common:
            webcam = os.path.join(self.webcam_path, frame)
            thermcam = os.path.join(self.thermcam_path, frame)
            output = os.path.join(self.montage_path, frame)
            all_frames.append(
                (webcam, thermcam, output, self.height, self.quality))

        pool = multiprocessing.Pool(self.threads)

        #
        # process_frame resizes and creates the montage
        #
        pool.map(process_frame, all_frames, chunksize=1)

    def generate_video(self):

        # Tweak to only do the thermcam
        input_path = self.thermcam_path

        #
        # Call ffmpeg to create the video
        #
        cmd = shlex.split("{ffmpeg:s} -y -threads {threads:d} -pattern_type glob -i '{input:s}/2*.{ext:s}' -r 240 -framerate 1/20 -vf \"setpts=0.5*PTS\" -vsync 2 -c:v libvpx -qmin 0 -qmax 50 -crf 5 -b:v 1M -c:a libvorbis {output:s}/{filename:s}".format(
            ffmpeg=self.ffmpeg, threads=self.threads, input=input_path, ext="webp", output=".", filename=self.output_name))
        out = subprocess.check_output(cmd)
        print(out)

    def upload_video(self):
        #
        # Upload video
        #
        desc = "Pomona Watcher"
        category = "15"
        all_files = sorted(self.common)
        first = all_files[0].split("T")[0]
        last = all_files[-1].split("T")[0]
        title = "Pomona - ({start:s} - {end:s})".format(start=first, end=last)

        cmd = shlex.split(
            'python upload_video.py --noauth_local_webserver --file="{file:s}" --title="{title:s}" --description="{desc:s}" --category="{category:s}"'.
            format(
                file=self.output_name, title=title, desc=desc,
                category=category))
        out = subprocess.check_output(cmd)
        print(out)

    def main(self):
        self.cleanup()
        self.find_common_files()

        # Do not need height
        # self.find_height()

        # Do not need to process frames
        # self.process_frames()

        self.generate_video()
        self.upload_video()


if __name__ == "__main__":
    MontageVideo().main()

# EOF
