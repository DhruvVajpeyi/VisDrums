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

def init_tracker(frame, tag, trackerFn):
    initBB = cv2.selectROI(tag, frame, fromCenter=False, showCrosshair=True)
    tracker = trackerFn()
    tracker.init(frame, initBB)
    return tracker

def get_overlapped_circles(circles, bbox):
    if circles is not None and bbox is not None:
        circles_list = np.round(circles[0, :]).astype("int")
        for idx, (circle_x, circle_y, circle_r) in enumerate(circles_list):
            if(check_overlap(circle_x, circle_y, circle_r, bbox)):
                return idx
    return -1

def check_overlap(circle_x, circle_y, circle_r, bbox):
    if bbox is None:
        return False

    circleDistanceX = abs(circle_x - (bbox[0]+bbox[2]/2))
    circleDistanceY = abs(circle_y - (bbox[1]+bbox[3]/2))

    if (circleDistanceX > (bbox[2]/2 + circle_r) or 
        circleDistanceY > (bbox[3]/2 + circle_r)):
        return False

    if (circleDistanceX <= bbox[2]/2 or
        circleDistanceY <= bbox[3]/2):
         return True

    cornerDistance_sq = (circleDistanceX - bbox[2]/2)**2 + (circleDistanceY - bbox[3]/2)**2

    return (cornerDistance_sq <= (circle_r**2))