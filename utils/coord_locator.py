# importing the module
import logging
import cv2
import numpy as np
from typing import List, Tuple


class CoordLocator:
    def __init__(self, image_name: str = None) -> None:
        # read image
        if image_name:
            self.image = cv2.imread(image_name)
        else:
            self.image = None

    def load_image(self, image_name) -> None:
        # read image
        self.image = cv2.imread(image_name)

    # function to display the coordinates of the points clicked on the image
    def mouse_click_event(self, event, x, y, flags, params) -> None:
        """Appends the clicked points to self.points list and overlays the
        points onto the image"""
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:

            # displaying the coordinates
            # on the Shell
            logging.info(f"({x}, {y})")

            # displaying the clicked points on the image window
            cv2.circle(self.image, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("Select points & press 'q'", self.image)
            self.points.append((x, y))

    def select_points(self, image: np.ndarray = None) -> List[Tuple]:
        """Displays the image and each clicked point is shown.
        X-Y coordinates of the ponts are returned as a list
        of tuples"""
        self.points = []
        if isinstance(image, str):
            self.image = self.image = cv2.imread(image)
        elif isinstance(image, np.ndarray):
            self.image = image
        # displaying the image
        cv2.imshow("Select points & press 'q'", self.image)

        # setting mouse handler for the image and calling
        # the mouse click_event() function
        cv2.setMouseCallback("Select points & press 'q'", self.mouse_click_event)

        # wait for a key to be pressed to exit
        cv2.waitKey(0)

        # close the window
        cv2.destroyAllWindows()
        return self.points

    def get_points(self) -> List[Tuple]:
        return self.points


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    cl = CoordLocator("utils/lena.png")
    pts = cl.select_points()
    logging.info(pts)
