import numpy as np
import cv2

cap = cv2.VideoCapture(0)
initBB = None
trackerFn = cv2.TrackerCSRT_create
tracker = None
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    (H, W) = frame.shape[:2]
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
            print('found')
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
            showCrosshair=True)
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        print('initing')
        tracker = trackerFn()
        tracker.init(frame, initBB)
        print('initialized')
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if key== ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()