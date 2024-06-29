import logging
from tkinter import Tk
from tkinter import messagebox as mb
import cv2
import numpy as np
from utils.coord_locator import CoordLocator


class Positioning:
    def __init__(self) -> None:
        self.homography = None
        self.img_coord_locator = CoordLocator()

    def load_homography(self, filename=None) -> None:
        """Load homography matrix from file"""
        try:
            if filename:
                self.homography = np.loadtxt(filename, delimiter=",", dtype=np.float32)
            else:
                self.homography = np.loadtxt(
                    "homography.csv", delimiter=",", dtype=np.float32
                )
        except FileNotFoundError:
            logging.warning("Homography file does not exist!")

    def save_homography(self, filename=None) -> None:
        """Save homography matrix to file"""
        if filename:
            np.savetxt(filename, self.homography, delimiter=",")
        else:
            np.savetxt("homography.csv", self.homography, delimiter=",")

    def calibrate(self, image, world_coordinates) -> None:
        """Calculate homography matrix that maps from 4 selected points on
        image to 4 points in real world"""
        root = Tk()
        root.withdraw()
        mb.showinfo(
            "Attention",
            "Select 4 points on image at positions (-1, 3), (1, 3), (-1, 1), (1, 1) in that specific order and press 'q'",
        )
        image_coordinates = self.img_coord_locator.select_points(image)
        self.homography = cv2.getPerspectiveTransform(
            np.array(image_coordinates, dtype=np.float32),
            np.array(world_coordinates, dtype=np.float32),
        )
        self.save_homography()

    def find_position(self, coordinates) -> np.ndarray:
        position = cv2.perspectiveTransform(
            np.array([coordinates], dtype=np.float32),
            self.homography,
        )
        return position


def main() -> None:
    i = [(-1, 1), (1, 1), (-1, 3), (1, 3)]
    w = [(-1, 1), (1, 1), (-1, 3), (1, 3)]
    pos = Positioning()
    pos.calibrate(i, w)


if __name__ == "__main__":
    main()
