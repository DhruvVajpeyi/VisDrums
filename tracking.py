import numpy as np
import cv2

def drawBB(tracker, frame, circles):
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

def detect_overlap(circle, bbox):
    if bbox is None:
        return False

    circleDistanceX = abs(circle['center'][0] - (bbox[0]+bbox[2]/2))
    circleDistanceY = abs(circle['center'][1] - (bbox[1]+bbox[3]/2))

    if (circleDistanceX > (bbox[2]/2 + circle['radius']) or 
        circleDistanceY > (bbox[3]/2 + circle['radius'])):
        return False

    if (circleDistanceX <= bbox[2]/2 or
        circleDistanceY <= bbox[3]/2):
         return True

    cornerDistance_sq = (circleDistanceX - bbox[2]/2)**2 + (circleDistanceY - bbox[3]/2)**2

    return (cornerDistance_sq <= (circle['radius']**2))

def initTracker(frame, tag, trackerFn):
    initBB = cv2.selectROI(tag, frame, fromCenter=False, showCrosshair=True)
    tracker = trackerFn()
    tracker.init(frame, initBB)
    return tracker

cap = cv2.VideoCapture(0)
trackerFn = cv2.TrackerCSRT_create
tracker1 = None
tracker2 = None

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    (H, W) = frame.shape[:2]
    circles = [
        {'center': (int(W/2), int(H/2)), 'radius': int(H/8)}
    ]
    
    bbox1 = drawBB(tracker1, frame, circles)
    bbox2 = drawBB(tracker2, frame, circles)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1 = initTracker(frame, "Tracker 1", trackerFn)
        tracker2 = initTracker(frame, "Tracker 2", trackerFn)


    # Display the resulting frame
    for circle in circles:
        if(detect_overlap(circle, bbox1)):
            print("OVERLAP1")
        if(detect_overlap(circle, bbox2)):
            print("OVERLAP2")
        cv2.circle(frame, circle['center'], circle['radius'], (0, 255, 0))
    cv2.imshow('frame',frame)
    if key== ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()