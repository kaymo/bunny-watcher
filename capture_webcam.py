#!/usr/bin/env python

# Dependencies: OpenCV
import cv2
import time
import datetime
import shutil
import os
import cv2.cv as cv
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

        self.FRAME_HEIGHT = 1536
        self.FRAME_WIDTH = 2304
        self.AUTO_BRIGHTNESS = 0.42
        self.AUTO_SATURATION = 0.46
        self.AUTO_CONTRAST = 0.46

        self.RGB_DARK_THRESHOLD = 40

        self.detect_camera_port()

    def detect_camera_port(self):
        name = "HD Pro Webcam C920"
        for camera in os.listdir("/sys/class/video4linux"):
            idx = camera.replace("video", "")
            sys_dir = os.path.realpath(os.path.join(
                "/sys/class/video4linux/", camera))
            name_file = os.path.join(sys_dir, "name")
            lines = open(name_file, "r").readlines()
            if name in lines[0]:
                self.CAMERA_PORT = int(idx)

    def get_image(self):
        """
        Captures a single image from the camera and returns it in PIL format
        """

        def get_property(property, property_id):
            # print "{}: {}".format(property, camera.get(property_id))
            pass

        # Open the camera device and create OpenCV object
        camera = cv2.VideoCapture(self.CAMERA_PORT)

        if False:
            # Get the initial amera properties
            get_property("width",      cv.CV_CAP_PROP_FRAME_WIDTH)
            get_property("height",     cv.CV_CAP_PROP_FRAME_HEIGHT)
            get_property("brightness", cv.CV_CAP_PROP_BRIGHTNESS)
            get_property("contrast",   cv.CV_CAP_PROP_CONTRAST)
            get_property("saturation", cv.CV_CAP_PROP_SATURATION)

        # Ensure that sensible values are set
        camera.set(cv.CV_CAP_PROP_BRIGHTNESS,   self.AUTO_BRIGHTNESS)
        camera.set(cv.CV_CAP_PROP_CONTRAST,     self.AUTO_CONTRAST)
        camera.set(cv.CV_CAP_PROP_SATURATION,   self.AUTO_SATURATION)
        camera.set(cv.CV_CAP_PROP_FRAME_WIDTH,  self.FRAME_WIDTH)
        camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)

        if False:
            get_property("brightness", cv.CV_CAP_PROP_BRIGHTNESS)
            get_property("contrast",   cv.CV_CAP_PROP_CONTRAST)
            get_property("saturation", cv.CV_CAP_PROP_SATURATION)
            get_property("width",      cv.CV_CAP_PROP_FRAME_WIDTH)
            get_property("height",     cv.CV_CAP_PROP_FRAME_HEIGHT)

        retval, image = camera.read()
        print retval

        # Discard any frames that are too dark
        if retval and len(image) and len(image[0]) and len(image[0][0]):

            # Keep image if the first pixel's avergae is greater than the threshold
            if sum(image[0][0]) / len(image[0][0]) > self.RGB_DARK_THRESHOLD:
                ret_val = True
            else:
                #
                # Keep image if the average pixel value is greater than a threshold
                #
                # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
                #
                avg_color_per_row = numpy.average(image, axis=0)
                avg_color_img = numpy.average(avg_color_per_row, axis=0)
                avg_pixel = numpy.average(avg_color_img, axis=0)

                if avg_pixel > self.RGB_DARK_THRESHOLD:
                    ret_val = True
                else:
                    ret_val = False

        del(camera)
        return ret_val, image

    def capture(self, time_now):
        """
        Capture image and output to filename based on time_now param
        """
        time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        [result, camera_capture] = self.get_image()

        if result:

            # Use the current time as the filename
            curr_time = time_now.isoformat().replace(".", "_").replace(":", "_")

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(camera_capture, time_str, (20, 70),
                        font, 2.5, (255, 255, 255), 4)

            # Store the image in the history and copy over the 'current' view

            output_img = os.path.join(
                self.CAPTURES_DIR, "{:s}.jpg".format(curr_time))
            cv2.imwrite(output_img, camera_capture,
                        [cv2.cv.CV_IMWRITE_JPEG_QUALITY, self.JPEG_QUALITY])
            shutil.copyfile(
                output_img, self.CURRENT_CAPTURE)
        else:
            curr_time = time_now.isoformat().replace(".", "_").replace(":", "_")
            print "Failed: " + curr_time


if __name__ == "__main__":
    time_now = datetime.datetime.now()

    webcam = CVWebcam("/tmp")
    webcam.capture(time_now)

# EOF
