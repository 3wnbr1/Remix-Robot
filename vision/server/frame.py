import time
from human_detector import findHuman, LargestRectangle


class Frame:
    """Image frame class."""

    def __init__(self, image):
        self.image = image
        self.date = time.time()
        self.processed = False
        self.rect = None

    def process(self):
        """Method to process the frame."""
        self.rect = findHuman(image)
