import cv2
import base64

RASPBERRY = False

def captureImage():
    """Capture image from raspberry pi."""
    if RASPBERRY:
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        camera = PiCamera()
        rawCapture = PiRGBArray(camera, size=(640, 480))
        # Initialize camera
        time.sleep(0.1)

        camera.capture(rawCapture, format="bgr")
        return rawCapture.array
    else:
        return cv2.imread("../test.bmp")

def imageAsBase64():
    _ ,img = cv2.imencode('.jpg', captureImage())
    return base64.b64encode(img)
