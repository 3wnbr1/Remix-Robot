import io
import cv2
import time
import base64

RASPBERRY = True

if RASPBERRY:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

    camera = PiCamera()
    camera.framerate = 5
    rawCapture = PiRGBArray(camera, size=(720, 480))
    time.sleep(2)

def captureImage():
    """Capture image from raspberry pi."""
    if RASPBERRY:
        rawCapture.truncate(0)
        for frame in camera.capture_continuous(rawCapture, format="bgr"):
            return frame.array
    else:
        return cv2.imread("../test.bmp")

def imageAsBase64():
    _ ,img = cv2.imencode('.jpg', captureImage())
    return base64.b64encode(img)
