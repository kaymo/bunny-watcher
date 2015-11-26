import cv2, time, datetime, shutil, os
import cv2.cv as cv
 
PORT = 0
FILE = "static/captures/image1.jpg"
INTERVAL = 10
JPEG_QUALITY = 85
CAPTURES_DIR = "static/captures/"
CURRENT_CAPTURE = CAPTURES_DIR + "current.jpg"

# Open the camera device and create OpenCV object
camera = cv2.VideoCapture(PORT)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():

    retval, im = camera.read()
    return retval, im

# Get and print an OpenCV property
def get_property( property, property_id ):
    
    print "{}: {}".format(property, camera.get(property_id))

# Get the initial amera properties
get_property("width",      cv.CV_CAP_PROP_FRAME_WIDTH)
get_property("height",     cv.CV_CAP_PROP_FRAME_HEIGHT)
get_property("brightness", cv.CV_CAP_PROP_BRIGHTNESS)
get_property("contrast",   cv.CV_CAP_PROP_CONTRAST)
get_property("saturation", cv.CV_CAP_PROP_SATURATION)

print

# Ensure that sensible values are set
camera.set(cv.CV_CAP_PROP_BRIGHTNESS,   0.42)
camera.set(cv.CV_CAP_PROP_CONTRAST,     0.46)
camera.set(cv.CV_CAP_PROP_SATURATION,   0.46)
camera.set(cv.CV_CAP_PROP_FRAME_WIDTH,  2304)
camera.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 1536)

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
        time.sleep(INTERVAL)

        # Grab the image
        [result, camera_capture] = get_image()
        
        # Overwrite the previous image
        if result:

            # Use the current time as the filename
            curr_time = datetime.datetime.now().isoformat().replace(".","_").replace(":","_")

            # Store the image in the history and copy over the 'current' view
            cv2.imwrite( CAPTURES_DIR + curr_time + ".jpg", camera_capture, [cv2.cv.CV_IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            shutil.copyfile( CAPTURES_DIR + curr_time + ".jpg", CURRENT_CAPTURE)
        
        # Delete if any images older than a day
        for fn in sorted(os.listdir( CAPTURES_DIR )):
            fp = os.path.join(CAPTURES_DIR, fn)
            if os.stat(fp).st_mtime < time.time() - 86400:
                if os.path.isfile(fp):
                    os.remove(fp)
            
            # The files are ordered by filename (by age) so stop if a young file is found 
            else:
                break

except KeyboardInterrupt:
    print "\nQuitting ..."

# Clean up
finally:
    del(camera)
