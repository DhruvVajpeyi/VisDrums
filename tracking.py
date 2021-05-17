import numpy as np
import cv2


"""Update the tracker with a new frame
args: tracker- CV2 tracker that was initialized on a ROI
      frame- The new frame
returns: bounding box of tracked object in new frame
"""
def draw_bb(tracker, frame):
    if tracker is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            # Draw the new bounding box on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)
            return box
    return None

"""Initialize tracker with a user selected Region of Interest
args: frame - The frame to select the object in
      tag - Name for the ROI selection window
returns: tracker
"""
def init_tracker(frame, tag):
    init_bb = cv2.selectROI(tag, frame, fromCenter=False, showCrosshair=True)
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, init_bb)
    return tracker

"""Get index of bbox overlapped circle
args: circles- List of circles to check for overlap. bbox- Bounding box of tracked object
returns: index of first circle that has overlap
"""
def get_overlapped_circles(circles, bbox):
    if circles is not None and bbox is not None:
        circles_list = np.round(circles[0, :]).astype("int")
        for idx, (circle_x, circle_y, circle_r) in enumerate(circles_list):
            if check_overlap(circle_x, circle_y, circle_r, bbox):
                return idx
    return -1

"""Check if bounding box center is inside circle
args: circle_x - x position of circle center
      circle_y - y position of circle center
      circle_r - circle radius
      bbox - bounding box of tracked object
returns true if bounding box center is inside circle
"""
def check_overlap(circle_x, circle_y, circle_r, bbox):
    mid_x = bbox[0] + bbox[2] / 2
    mid_y = bbox[1] + bbox[3] / 2

    return ((circle_x-mid_x)**2 + (circle_y-mid_y)**2 <= circle_r**2)

"""Check if bounding box center is below line
args: line_y - y position of line
      bbox - bounding box of tracked object
returns true if bounding box center is below line
"""
def check_if_below_line(line_y, bbox):
    if bbox is None or bbox[1] is None or bbox[3] is None:
        return False
    return line_y < (bbox[1] + bbox[3] / 2)

"""Check if bounding box center is above line
args: line_y - y position of line
      bbox - bounding box of tracked object
returns true if bounding box center is above line
"""
def check_if_reset_line(line_y, bbox, current):
    if bbox is None or bbox[1] is None or bbox[3] is None:
        return False
    if line_y > (bbox[1] + bbox[3] / 2):
        return True
    return current
