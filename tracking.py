import numpy as np
import cv2

def drawBB(tracker, frame, circles):
    (x, y, w, h) = (0, 0, 0, 0)
    if tracker is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)
    for circle in circles:
        if(np.linalg.norm(np.array((x, y))-np.array(circle['center'])) < circle['radius']):
            print("OVERLAP")
        cv2.circle(frame, circle['center'], circle['radius'], (0, 255, 0))

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
    
    drawBB(tracker1, frame, circles)
    drawBB(tracker2, frame, circles)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1 = initTracker(frame, "Tracker 1", trackerFn)
        tracker2 = initTracker(frame, "Tracker 2", trackerFn)


    # Display the resulting frame
    cv2.imshow('frame',frame)
    if key== ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()