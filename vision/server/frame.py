import time
from human_detector import findHuman, LargestRectangle, exentrationPercentage, heightPercentage, distanceToObject


MAX_SPEED = 255
SPEED_FACTOR = 100
TIME = 0.3

EXENTRATION_THRESHOLD = 0.1
HEIGHT_THRESHOLD = 0.75


class Frame:
    """Image frame class."""

    def __init__(self, image):
        self.image = image
        self.date = time.time()
        self.processed = False

    def process(self):
        """Method to process the frame."""
        self.rect = LargestRectangle(findHuman(self.image))
        self.extentration = exentrationPercentage(self.image, self.rect)
        self.heigt = heightPercentage(self.image, self.rect)
        self.processed = True
        self.distance = distanceToObject(self.rect)
        self.forward = None

    def giveDirection(self):
        """Giving direction to the robot. -> v_right, v_left, time."""
        if self.heigt < HEIGHT_THRESHOLD or abs(self.extentration) > EXENTRATION_THRESHOLD:
            return str(self.extentration) + "," + str(self.distance) + ",1"
        return "0,0,0"
