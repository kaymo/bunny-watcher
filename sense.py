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

CAMERA_PORT = 0
CAPTURES_DIR = "static/captures/"
CURRENT_CAPTURE = CAPTURES_DIR + "current.jpg"
INTERVAL = 60
JPEG_QUALITY = 85

FRAME_HEIGHT = 1536
FRAME_WIDTH = 2304
AUTO_BRIGHTNESS = 0.42
AUTO_SATURATION = 0.46
AUTO_CONTRAST = 0.46

RGB_DARK_THRESHOLD = 40

# Captures a single image from the camera and returns it in PIL format

@profile
def get_image():

    retval, image = camera.read()

    # Discard any frames that are too dark
    if retval and len(image) and len(image[0]) and len(image[0][0]):

        # Keep image if the first pixel's avergae is greater than the threshold
        if sum(image[0][0]) / len(image[0][0]) > RGB_DARK_THRESHOLD:
            return True, image

	#
        # Keep image if the average pixel value is greater than a threshold
	#
	# https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
	#
	avg_color_per_row = numpy.average(image, axis=0)
	avg_color_img = numpy.average(avg_color_per_row, axis=0)
	avg_pixel = numpy.average(avg_color_img, axis=0)

        if avg_pixel > RGB_DARK_THRESHOLD:
            return True, image

    return False, image

# Get and print an OpenCV property


def get_property(property, property_id):
    print "{}: {}".format(property, camera.get(property_id))

# Open the camera device and create OpenCV object
camera = cv2.VideoCapture(CAMERA_PORT)

# Get the initial amera properties
get_property("width",      cv.CV_CAP_PROP_FRAME_WIDTH)
get_property("height",     cv.CV_CAP_PROP_FRAME_HEIGHT)
get_property("brightness", cv.CV_CAP_PROP_BRIGHTNESS)
get_property("contrast",   cv.CV_CAP_PROP_CONTRAST)
get_property("saturation", cv.CV_CAP_PROP_SATURATION)

print

# Ensure that sensible values are set
camera.set(cv.CV_CAP_PROP_BRIGHTNESS,   AUTO_BRIGHTNESS)
camera.set(cv.CV_CAP_PROP_CONTRAST,     AUTO_CONTRAST)
camera.set(cv.CV_CAP_PROP_SATURATION,   AUTO_SATURATION)
camera.set(cv.CV_CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH)
camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

get_property("brightness", cv.CV_CAP_PROP_BRIGHTNESS)
get_property("contrast",   cv.CV_CAP_PROP_CONTRAST)
get_property("saturation", cv.CV_CAP_PROP_SATURATION)
get_property("width",      cv.CV_CAP_PROP_FRAME_WIDTH)
get_property("height",     cv.CV_CAP_PROP_FRAME_HEIGHT)

# Capture a still at regular intervals
print
print("Capturing images ...")

@profile
def main():

    global camera

    try:
        while 1:
            print "LOOP"
            start = datetime.datetime.now()
            # Grab the image
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            [result, camera_capture] = get_image()

            if result:

                # Use the current time as the filename
                curr_time = datetime.datetime.now().isoformat().replace(".", "_").replace(":", "_")

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(camera_capture, time_str, (20, 70),
                            font, 2.5, (255, 255, 255), 4)

                # Store the image in the history and copy over the 'current' view
                cv2.imwrite(CAPTURES_DIR + curr_time + ".jpg", camera_capture,
                            [cv2.cv.CV_IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
                shutil.copyfile(CAPTURES_DIR + curr_time + ".jpg", CURRENT_CAPTURE)
            else:
                curr_time = datetime.datetime.now().isoformat().replace(".", "_").replace(":", "_")
                print "Failed: " + curr_time

            # Delete if any images older than a day
            for fn in sorted(os.listdir(CAPTURES_DIR)):
                fp = os.path.join(CAPTURES_DIR, fn)
                if os.stat(fp).st_mtime < time.time() - 86400:
                    if os.path.isfile(fp):
                        os.remove(fp)

                # The files are ordered by filename (by age) so stop if a young
                # file is found
                else:
                    break

            end = datetime.datetime.now()
            elapsed = end - start

            interval = datetime.timedelta(seconds=INTERVAL)

            sleep_cnt = interval - elapsed

            time.sleep(sleep_cnt.total_seconds())

    except KeyboardInterrupt:
        print "\nQuitting ..."

    # Clean up
    finally:
        del(camera)

main()

# EOF
