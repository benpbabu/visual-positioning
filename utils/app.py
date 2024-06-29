import logging
from tkinter import Tk
from tkinter import messagebox as mb
import numpy as np
import cv2
from utils.coord_locator import CoordLocator
from utils.positioning import Positioning
from utils.video_handler import VideoDevice
from ultralytics import YOLO


class VisualPositioningApp:
    def __init__(self) -> None:
        self.coord_locator = CoordLocator()
        self.positioning = Positioning()
        self.positioning.load_homography()
        self.video_handler = VideoDevice()
        self.model = YOLO("yolov8n-seg.pt")
        self.colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
        ]

    def loop(self) -> None:
        while True:
            frame = self.video_handler.read()
            if frame is None:
                break
            results = self.model.predict(frame)[0]
            for box in results.boxes:
                # if box.id is None:
                #     continue
                color = self.colors[int(box.cls[0].item()) % len(self.colors)]
                # color = (0, 0, 255)
                name = results.names[box.cls[0].item()]
                position = box.xyxy[0].tolist()
                object_position = ((position[0] + position[2]) / 2, position[3])
                print("object position: ", object_position)
                world_coordinate = self.positioning.find_position([object_position])
                x_coordinate = world_coordinate[0][0][0]
                y_coordinate = world_coordinate[0][0][1]
                position_text = f"({x_coordinate:.2f},{y_coordinate:.2f})"
                cv2.rectangle(
                    img=frame,
                    pt1=(int(position[0]), int(position[1])),
                    pt2=(int(position[2]), int(position[3])),
                    color=color,
                    thickness=2,
                )
                cv2.putText(
                    img=frame,
                    text=name,
                    org=(int(position[0] + 5), int(position[1] + 20)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=color,
                    thickness=2,
                )
                cv2.putText(
                    img=frame,
                    text=position_text,
                    org=(int(position[0] + 5), int(position[1] + 50)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.75,
                    color=color,
                    thickness=2,
                )

            cv2.imshow("Camera feed", frame)
            if cv2.waitKey(1) == ord("q"):
                break

    def perform_calibration(self):
        frame = self.video_handler.get_specific_frame()
        self.positioning.calibrate(frame, [(-1, 3), (1, 3), (-1, 1), (1, 1)])

    def run(self):
        if self.positioning.homography is None:
            root = Tk()
            root.withdraw()
            answer = mb.askquestion(
                title="Homography not found", message="Proceed to calibrate?"
            )
            if answer == "yes":
                self.perform_calibration()
            else:
                return
        self.loop()


if __name__ == "__main__":
    app = VisualPositioningApp()
    app.run()
