import logging
from tkinter import Tk
from tkinter import messagebox as mb
import cv2
import numpy as np


MAX_VIDEO_DEVICE = 10


class VideoDevice:
    def __init__(self) -> None:
        self.load_device_info()
        self.open_video_device()

    def load_device_info(self):
        """Opens the saved video index file and loads the index value"""
        try:
            with open("video_device.txt", "r") as fh:
                self.video_device = int(fh.read())
        except FileNotFoundError:
            logging.warning(
                "video_device.txt not found. Assuming device0 and creating video_device.txt"
            )
            self.video_device = 0
            self.save_device_info()

    def save_device_info(self):
        """Saves the index of detected video device to file"""
        with open("video_device.txt", "w") as fh:
            fh.write(str(self.video_device))

    def find_video_device(self) -> int:
        """Find valid video devices and returns the index of available device.
        If there are more than one devices, the one with the highest index is
        returned. That way external cameras are given preference.
        """
        # iterate over multiple device indices and check if they return image
        for device in range(MAX_VIDEO_DEVICE):
            cap = cv2.VideoCapture(device)
            ret, _ = cap.read()
            if ret:
                self.video_device = device
                cap.release()
        self.save_device_info()

    def open_video_device(self) -> None:
        """Open video device for reading frames"""
        self.camera = cv2.VideoCapture(self.video_device)

    def read(self) -> np.ndarray:
        """Read one video frame from device"""
        ret, frame = self.camera.read()
        if ret:
            return frame
        else:
            self.camera.release()
            return None

    def get_specific_frame(self) -> np.ndarray:
        """Displays the camera feed and returns the frame when q is pressed"""
        root = Tk()
        root.withdraw()
        mb.showinfo("Attention", "Select a frame by pressing 'q' on keyboard")
        selected = False
        while True:
            ret, frame = self.camera.read()
            if ret:
                cv2.imshow("Camera feed: Press 'q' to select", frame)
                if cv2.waitKey(1) == ord("q"):
                    selected = True
                    break
        cv2.destroyAllWindows()
        if selected:
            return frame
        else:
            self.camera.release()
            return None

    def close(self) -> None:
        """Release device resource"""
        self.camera.release()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    vid = VideoDevice()
    frame = vid.get_specific_frame()
    cv2.imshow("selected", frame)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    vid.close()
