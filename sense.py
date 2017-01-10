#!/usr/bin/env python

# Dependencies: OpenCV
import cv2, time, datetime, shutil, os
import cv2.cv as cv
 
CAMERA_PORT = 0
CAPTURES_DIR = "static/captures/"
CURRENT_CAPTURE = CAPTURES_DIR + "current.jpg"
INTERVAL = 60
JPEG_QUALITY = 85

FRAME_HEIGHT = 1536
FRAME_WIDTH = 2304
AUTO_BRIGHTNESS = 0.42
AUTO_SATURATION = 0.46
AUTO_CONTRAST   = 0.46

RGB_DARK_THRESHOLD = 40
 
# Captures a single image from the camera and returns it in PIL format
def get_image():

    retval, image = camera.read()

    # Discard any frames that are too dark
    if retval and len(image) and len(image[0]) and len(image[0][0]):
        
        # Keep image if the first pixel's avergae is greater than the threshold
        if sum(image[0][0]) / len(image[0][0]) > RGB_DARK_THRESHOLD:
            return True, image

        # Keep image if the average pixel value is greater than a threshold
        temp_pixels = [pixel for row in image for column in row for pixel in column]
        avg_pixel = sum(temp_pixels) / len(image) / len(image[0]) / len(image[0][0])
        if avg_pixel > RGB_DARK_THRESHOLD:
            return True, image 
             
    return False, image

# Get and print an OpenCV property
def get_property( property, property_id ):    
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

try:
    while 1:
        # Grab the image
        [result, camera_capture] = get_image()
        
        if result:

            # Use the current time as the filename
            curr_time = datetime.datetime.now().isoformat().replace(".","_").replace(":","_")

            # Store the image in the history and copy over the 'current' view
            cv2.imwrite( CAPTURES_DIR + curr_time + ".jpg", camera_capture, [cv2.cv.CV_IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            shutil.copyfile( CAPTURES_DIR + curr_time + ".jpg", CURRENT_CAPTURE)
        else:
            curr_time = datetime.datetime.now().isoformat().replace(".","_").replace(":","_")
            print "Failed: " + curr_time
        
        # Delete if any images older than a day
        for fn in sorted(os.listdir( CAPTURES_DIR )):
            fp = os.path.join(CAPTURES_DIR, fn)
            if os.stat(fp).st_mtime < time.time() - 86400:
                if os.path.isfile(fp):
                    os.remove(fp)
            
            # The files are ordered by filename (by age) so stop if a young file is found 
            else:
                break

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print "\nQuitting ..."

# Clean up
finally:
    del(camera)

# EOF
