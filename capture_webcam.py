#!/usr/bin/env python

# Dependencies: OpenCV
from __future__ import print_function
from builtins import str
from builtins import object
import cv2
# from cv2 import cv
import time
import datetime
import shutil
import os
# import cv2.cv as cv
import numpy

if 'profile' not in globals():
    def profile(func):
        return func


class CVWebcam(object):

    def __init__(self, capture_location):

        self.CAMERA_PORT = None
        self.CAPTURES_DIR = capture_location
        self.INTERVAL = 60

        self.FRAME_WIDTH = 1280 # 2304
        self.FRAME_HEIGHT = 800 # 1536
        self.AUTO_BRIGHTNESS = 0.5
        self.AUTO_SATURATION = 0.5
        self.AUTO_CONTRAST = 10

        self.RGB_DARK_THRESHOLD = 40

        self.IMAGE_QUALITY = 100
        self.IMAGE_FORMAT = cv2.IMWRITE_WEBP_QUALITY

        self.unsharp = True
        self.convert = True
        self.save_fmt = "webp"
        self.display_fmt = "jpg"
        self.name = "Web"


    def detect_camera_port(self):
        name = "LifeCam HD-3000"
        for camera in sorted(os.listdir("/sys/class/video4linux")):
            idx = camera.replace("video", "")
            sys_dir = os.path.realpath(os.path.join(
                "/sys/class/video4linux/", camera))
            name_file = os.path.join(sys_dir, "name")
            lines = open(name_file, "r").readlines()
            if name in lines[0]:
                self.CAMERA_PORT = int(idx)
                break

    def get_image(self):
        """
        Captures a single image from the camera and returns it in PIL format
        """

        def get_property(camera, property_str, property_id):
            print("{}: {}".format(property_str, camera.get(property_id)))

        self.detect_camera_port()

        # Open the camera device and create OpenCV object
        camera = cv2.VideoCapture(self.CAMERA_PORT)

        if False:
            # Get the initial amera properties
            get_property("width",      cv2.CAP_PROP_FRAME_WIDTH)
            get_property("height",     cv2.CAP_PROP_FRAME_HEIGHT)
            get_property("brightness", cv2.CAP_PROP_BRIGHTNESS)
            get_property("contrast",   cv2.CAP_PROP_CONTRAST)
            get_property("saturation", cv2.CAP_PROP_SATURATION)

        if False:
            # Ensure that sensible values are set
            camera.set(cv2.CAP_PROP_BRIGHTNESS,   self.AUTO_BRIGHTNESS)
            camera.set(cv2.CAP_PROP_CONTRAST,     self.AUTO_CONTRAST)
            camera.set(cv2.CAP_PROP_SATURATION,   self.AUTO_SATURATION)

        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  self.FRAME_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)

        get_property(camera, "brightness", cv2.CAP_PROP_BRIGHTNESS)
        get_property(camera, "contrast",   cv2.CAP_PROP_CONTRAST)
        get_property(camera, "saturation", cv2.CAP_PROP_SATURATION)
        get_property(camera, "width",      cv2.CAP_PROP_FRAME_WIDTH)
        get_property(camera, "height",     cv2.CAP_PROP_FRAME_HEIGHT)

        IGNORE = camera.read()
        ret_val, image = camera.read()
        # print "Camera read returned: ", str(ret_val)
        camera.release()
        del(camera)
        return ret_val, image

    def capture(self, time_now):
        """
        Capture image and output to filename based on time_now param
        """
        time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        [result, camera_capture] = self.get_image()
        print("{name:s}: get_image returned: {value:s}".format(name=self.name, value=str(result)))

        if result:

            # Use the current time as the filename
            fdate = time_now.isoformat().replace(".", "_").replace(":", "_")

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(camera_capture, time_str, (12, 40),
                    font, 1.2, (40, 60, 215), 2, cv2.LINE_AA)

            # Store the image in the history and copy over the 'current' view

            output_base_name = os.path.join(
                self.CAPTURES_DIR, "{:s}".format(fdate))
            output_img = "{name:s}.{save_fmt:s}".format(name=output_base_name, save_fmt=self.save_fmt)
            imwrite_ret = cv2.imwrite(output_img, camera_capture,
                         [self.IMAGE_FORMAT, self.IMAGE_QUALITY])
            print("{name:s}: cv2.imwrite returned: {value:s}".format(name=self.name, value=str(imwrite_ret)))
            if self.unsharp:
                cmd = "convert -unsharp 10x4+1+0 {fname:s} {fname:s}".format(fname=output_img)
                system_ret = os.system(cmd)
                print("{name:s}: os.system (unsharp) returned: {value:s}".format(name=self.name, value=str(system_ret)))
            if self.convert:
                cmd = "convert -quality 85 {fname:s}.{save_fmt:s} {fname:s}.{display_fmt:s}".format(fname=output_base_name, save_fmt=self.save_fmt, display_fmt=self.display_fmt)
                system_ret = os.system(cmd)
                print("{name:s}: os.system (convert) returned: {value:s}".format(name=self.name, value=str(system_ret)))


        else:
            curr_time = time_now.isoformat().replace(".", "_").replace(":", "_")
            print("No result for webcam at " + curr_time)


if __name__ == "__main__":
    while True:
        time_now = datetime.datetime.now()
        print(str(time_now))
        webcam = CVWebcam("static/captures/webcam")
        webcam.capture(time_now)
        break
        time.sleep(2)

# EOF
