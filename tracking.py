import numpy as np
import cv2


def draw_bb(tracker, frame, circles):
    if tracker is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (255, 255, 0), 2)
            check_overlap(circles, x, y)


def init_tracker(frame, tag, tracker_fn):
    init_bb = cv2.selectROI(tag, frame, fromCenter=False, showCrosshair=True)
    tracker = tracker_fn()
    tracker.init(frame, init_bb)
    return tracker


def check_overlap(circles, box_x, box_y):
    if circles is not None:
        circles_list = np.round(circles[0, :]).astype("int")
        for (circle_x, circle_y, circle_r) in circles_list:
            if (box_x - circle_x) * (box_x - circle_x) + (box_y - circle_y) * (box_y - circle_y) <= circle_r * circle_r:
                print("OVERLAP")
