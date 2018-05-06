#!/usr/bin/env python

# Dependencies: OpenCV
import cv2
import time
import datetime
import shutil
import os
import cv2.cv as cv
import numpy

from capture_webcam import CVWebcam


class BunnySense(object):

    def __init__(self, output_dir, interval):
        self.CAPTURES_DIR = output_dir
        self.webcam = CVWebcam(output_dir)
        self.INTERVAL = interval

    def main(self):

        try:
            while 1:
                print "LOOP"
                time_now = datetime.datetime.now()

                self.webcam.capture(time_now)

                # Delete if any images older than a day
                for fn in sorted(os.listdir(self.CAPTURES_DIR)):
                    fp = os.path.join(self.CAPTURES_DIR, fn)
                    if os.stat(fp).st_mtime < time.time() - 86400:
                        if os.path.isfile(fp):
                            os.remove(fp)

                    # The files are ordered by filename (by age) so stop if a young
                    # file is found
                    else:
                        break

                end = datetime.datetime.now()
                elapsed = end - time_now

                interval = datetime.timedelta(seconds=self.INTERVAL)

                sleep_cnt = interval - elapsed

                time.sleep(sleep_cnt.total_seconds())

        except KeyboardInterrupt:
            print "\nQuitting ..."


if __name__ == "__main__":
    capture_dir = "/tmp"
    bunny_sense = BunnySense(capture_dir, 10)
    bunny_sense.main()

# EOF
