import io
import cv2
import time
import base64

RASPBERRY = False

if RASPBERRY:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 1
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(2)

def captureImage():
    """Capture image from raspberry pi."""
    if RASPBERRY:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            rawCapture.truncate(0)
            return image
    else:
        return cv2.imread("../test.bmp")

def imageAsBase64():
    _ ,img = cv2.imencode('.jpg', captureImage())
    return base64.b64encode(img)
