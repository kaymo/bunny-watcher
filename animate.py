import os

CAPTURES_DIR = "/home/pi/bunny-watcher/static/captures"

try:

    # Create .gif
    os.system("ffmpeg -y -framerate 10 -pattern_type glob -i '{}/2*.jpg' -pix_fmt rgb8 -ignore_loop 0 -s 576x384 {}/animated.gif".format(CAPTURES_DIR, CAPTURES_DIR) )

except KeyboardInterrupt:
    print "Quitting ..."
