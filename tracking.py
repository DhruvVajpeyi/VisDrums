import numpy as np
import cv2


def draw_bb(tracker, frame):
    if tracker is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)
            return box
    return None


def init_tracker(frame, tag):
    init_bb = cv2.selectROI(tag, frame, fromCenter=False, showCrosshair=True)
    param_handler = cv2.TrackerCSRT_Params()
    setattr(param_handler, 'background_ratio', 0)
    print(param_handler)
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, init_bb)
    return tracker


def get_overlapped_circles(circles, bbox):
    if circles is not None and bbox is not None:
        circles_list = np.round(circles[0, :]).astype("int")
        for idx, (circle_x, circle_y, circle_r) in enumerate(circles_list):
            if check_overlap(circle_x, circle_y, circle_r, bbox):
                return idx
    return -1


def check_overlap(circle_x, circle_y, circle_r, bbox):
    if bbox is None:
        return False

    circle_distance_x = abs(circle_x - (bbox[0] + bbox[2] / 2))
    circle_distance_y = abs(circle_y - (bbox[1] + bbox[3] / 2))

    if (circle_distance_x > (bbox[2] / 2 + circle_r) or
            circle_distance_y > (bbox[3] / 2 + circle_r)):
        return False

    if (circle_distance_x <= bbox[2] / 2 or
            circle_distance_y <= bbox[3] / 2):
        return True

    corner_distance_sq = (circle_distance_x - bbox[2] / 2) ** 2 + (circle_distance_y - bbox[3] / 2) ** 2

    return corner_distance_sq <= (circle_r ** 2)


def check_if_below_line(line_y, bbox):
    if bbox is None or bbox[1] is None or bbox[3] is None:
        return False
    return line_y < (bbox[1] + bbox[3] / 2)


def check_if_reset_line(line_y, bbox, current):
    if bbox is None or bbox[1] is None or bbox[3] is None:
        return False
    if line_y > (bbox[1] + bbox[3] / 2):
        return True
    return current
