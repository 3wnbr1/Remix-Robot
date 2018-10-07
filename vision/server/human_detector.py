import cv2
import numpy as np
from imutils.object_detection import non_max_suppression


FOCAL = 60
HUMAN_WIDTH = 10


# Initialize detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def NMS(hog_rects_results):
    """Use Non-Max-Suppression. Ouput is format (xa, ya, xb, yb)."""
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in hog_rects_results])
    return non_max_suppression(rects, probs=None, overlapThresh=0.65)


def findHuman(image):
    """Returns the coordinates of a human person in an image with NMS applied."""
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(16, 16), scale=1.15)
    return NMS(rects)


def LargestRectangle(rects):
    """Returns the coordinates of the biggest detected rectangle."""
    surfaces = []
    for rect in rects:
        surfaces.append((rect[0]-rect[2]) * (rect[1]-rect[3]))
    try:
        rect = rects[surfaces.index(max(surfaces))]
    except ValueError:
        rect = None
    return rect


def exentrationPercentage(image, rect):
    """Return exentration in percent, can be negative."""
    if rect is None:
        return 0
    x = image.shape[1]
    center = rect[2] - rect[0] - x/2
    return round(center / x, 2)


def distanceToObject(rect):
    """Return approximate distance to object in meters."""
    return round((HUMAN_WIDTH*FOCAL)/(rect[2] - rect[0]), 2)
