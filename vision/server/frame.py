import time
from human_detector import findHuman, LargestRectangle, exentrationPercentage, heightPercentage


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
        self.forward = None

    def giveDirection(self):
        """Giving direction to the robot. -> v_right, v_left, time."""
        if self.heigt >= HEIGHT_THRESHOLD:
            return "0,0,0"
        else:
            if abs(self.extentration) <= EXENTRATION_THRESHOLD:
                return "0,0,0"
            else:
                if self.extentration > 0:
                    return str(MAX_SPEED)+","+str(MAX_SPEED-self.extentration*SPEED_FACTOR)+","+str(TIME)
                else:
                    return str(MAX_SPEED+self.extentration*SPEED_FACTOR)+","+str(MAX_SPEED)+","+str(TIME)
