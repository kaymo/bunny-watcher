#!/usr/bin/env python

# Dependencies: OpenCV
import cv2
import time
import datetime
import shutil
import os
import cv2.cv as cv
import numpy
import sys
from multiprocessing import Process

from capture_webcam import CVWebcam
from capture_therm import UVCThermCam, uvc_setup

bunny_sense = None
time_now = None


def capture_webcam():
    global bunny_sense
    global time_now

    bunny_sense.webcam.capture(time_now)


def capture_thermcam():
    global bunny_sense
    global time_now

    bunny_sense.thermcam.capture(time_now)


class BunnySense(object):

    def __init__(self, output_dir, interval):
        self.CAPTURES_DIR = output_dir
        self.webcam_dir = os.path.join(output_dir, "webcam")
        self.thermcam_dir = os.path.join(output_dir, "thermcam")
        if not os.path.exists(self.webcam_dir):
            os.makedirs(self.webcam_dir)
        if not os.path.exists(self.thermcam_dir):
            os.makedirs(self.thermcam_dir)
        self.webcam = CVWebcam(self.webcam_dir)
        self.thermcam = UVCThermCam(self.thermcam_dir)
        self.INTERVAL = interval

    def clean_dir(self, dir_to_clean):

        # Delete if any images older than a day
        for fn in sorted(os.listdir(dir_to_clean)):
            fp = os.path.join(dir_to_clean, fn)
            if os.stat(fp).st_mtime < time.time() - 86400:
                if os.path.isfile(fp):
                    os.remove(fp)

            # The files are ordered by filename (by age) so stop if a young
            # file is found
            else:
                break

    def main(self):
        global time_now

        while True:
            try:
                time_now = datetime.datetime.now()
                print "LOOP", str(time_now)

                p_webcam = Process(target=capture_webcam)
                p_thermcam = Process(target=capture_thermcam)
                p_webcam.start()
                p_thermcam.start()
                p_webcam.join()
                p_thermcam.join()

                self.clean_dir(self.webcam_dir)
                self.clean_dir(self.thermcam_dir)

                end = datetime.datetime.now()
                elapsed = end - time_now

                interval = datetime.timedelta(seconds=self.INTERVAL)

                sleep_cnt = interval - elapsed

                time.sleep(sleep_cnt.total_seconds())

            except KeyboardInterrupt as _:
                print "\nQuitting ..."
                break
            except Exception as e:
                print str(e)
                continue


if __name__ == "__main__":
    with uvc_setup():
        capture_dir = "./static/captures"
        bunny_sense = BunnySense(capture_dir, 20)
        bunny_sense.main()

# EOF
