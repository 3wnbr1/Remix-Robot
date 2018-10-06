import cv2
import numpy as np
from imutils.object_detection import non_max_suppression


# Initialize detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def NMS(hog_rects_results):
    """Use Non-Max-Suppression. Ouput is format (xa, ya, xb, yb)."""
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in hog_rects_results])
    return non_max_suppression(rects, probs=None, overlapThresh=0.65)


def findHuman(image):
    """Returns the coordinates of a human person in an image with NMS applied."""
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    return NMS(rects)


# Load test image
image = cv2.imread("test.bmp")
(height, width) = image.shape[:-1]