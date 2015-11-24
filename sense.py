import cv2
import cv2.cv as cv
 
PORT = 0
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
camera = cv2.VideoCapture(PORT)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():

    retval, im = camera.read()
    return im

def get_property( property, property_id ):
    
    print "{}: {}".format(property, camera.get(property_id))

# Camera properties
get_property("width",      cv.CV_CAP_PROP_FRAME_WIDTH)
get_property("height",     cv.CV_CAP_PROP_FRAME_HEIGHT)
get_property("brightness", cv.CV_CAP_PROP_BRIGHTNESS)
get_property("contrast",   cv.CV_CAP_PROP_CONTRAST)
get_property("saturation", cv.CV_CAP_PROP_SATURATION)

print

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

print

# Take the image 
print("Taking image...")
camera_capture = get_image()

file = "static/captures/image1.jpg"
cv2.imwrite(file, camera_capture)
 
# Clean up
del(camera)
