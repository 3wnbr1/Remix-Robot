import time
from human_detector import findHuman, LargestRectangle, exentrationPercentage, distanceToObject, preprocess


MAX_SPEED = 255
SPEED_FACTOR = 100
TIME = 0.3

EXENTRATION_THRESHOLD = 0.05
DISTANCE_THRESHOLD = 1


class Frame:
    """Image frame class."""

    def __init__(self, image):
        self.image = image
        self.date = time.time()
        self.processed = False
        self.retrieved = False

    def process(self):
        """Method to process the frame."""
        self.image = preprocess(self.image)
        self.rect = LargestRectangle(findHuman(self.image))
        if self.rect is not None:
            self.extentration = exentrationPercentage(self.image, self.rect)
            self.processed = True
            self.distance = distanceToObject(self.rect)
        else:
            self.extentration = None
            self.processed = True
            self.distance = None
            self.forward = None

    def giveDirection(self):
        """Giving direction to the robot. -> v_right, v_left, time."""

        if self.rect is not None and not self.retrieved:
            if self.distance > DISTANCE_THRESHOLD or abs(self.extentration) > EXENTRATION_THRESHOLD:
                self.retrieved = True
                return str(self.extentration) + "," + str(self.distance) + ",1"
        return "0,0,0"
