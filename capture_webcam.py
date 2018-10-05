#!/usr/bin/env python

# Dependencies: OpenCV
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
        self.CURRENT_CAPTURE = os.path.join(self.CAPTURES_DIR, "current.jpg")
        self.INTERVAL = 60
        self.JPEG_QUALITY = 85

        self.FRAME_WIDTH = 1280 # 2304
        self.FRAME_HEIGHT = 800 # 1536
        self.AUTO_BRIGHTNESS = 0.5
        self.AUTO_SATURATION = 0.5
        self.AUTO_CONTRAST = 10

        self.RGB_DARK_THRESHOLD = 40


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
            print "{}: {}".format(property_str, camera.get(property_id))

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
        print "Camera read returned: ", str(ret_val)
        camera.release()
        del(camera)
        return ret_val, image

    def capture(self, time_now):
        """
        Capture image and output to filename based on time_now param
        """
        time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        [result, camera_capture] = self.get_image()
        print "get_image returned: ", str(result)

        if result:

            # Use the current time as the filename
            fdate = time_now.isoformat().replace(".", "_").replace(":", "_")

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(camera_capture, time_str, (12, 40),
                    font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

            # Store the image in the history and copy over the 'current' view

            output_img = os.path.join(
                self.CAPTURES_DIR, "{:s}.jpg".format(fdate))
            imwrite_ret = cv2.imwrite(output_img, camera_capture,
                        [cv2.IMWRITE_JPEG_QUALITY, self.JPEG_QUALITY])
            print "cv2.imwrite returned: ", imwrite_ret
            cmd = "convert -unsharp 10x4+1+0 {fname:s} {fname:s}".format(fname=output_img)
            system_ret = os.system(cmd)
            print "os.system returned: ", system_ret
            copy_ret = shutil.copyfile(
                output_img, self.CURRENT_CAPTURE)
            print "shutil.copyfile returned: ", copy_ret
        else:
            curr_time = time_now.isoformat().replace(".", "_").replace(":", "_")
            print "No result for webcam at " + curr_time


if __name__ == "__main__":
    while True:
        time_now = datetime.datetime.now()
        print str(time_now)
        webcam = CVWebcam("static/captures/webcam")
        webcam.capture(time_now)
        break
        time.sleep(2)

# EOF
