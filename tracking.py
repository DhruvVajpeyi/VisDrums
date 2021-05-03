import numpy as np
import cv2

def drawBB(initBB, tracker, frame, masked):
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(masked)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)
            

cap = cv2.VideoCapture(0)
initBB1 = None
initBB2 = None
trackerFn = cv2.TrackerCSRT_create
tracker1 = None
tracker2 = None
mask = None
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    (H, W) = frame.shape[:2]
    if mask is None:
        print(frame.shape)
        mask = np.zeros((H, W), dtype="uint8")
        cv2.circle(mask, (int(W/2), int(H/2)), int(H/8), 255, thickness=-1)
    masked_img = cv2.bitwise_and(frame,frame,mask = mask)
    drawBB(initBB1, tracker1, frame, masked_img)
    drawBB(initBB2, tracker2, frame, masked_img)
    cv2.circle(frame, (int(W/2), int(H/2)), int(H/8), (255, 0, 0))
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB1 = cv2.selectROI("Frame1", frame, fromCenter=False,
            showCrosshair=True)
        initBB2 = cv2.selectROI("Frame2", frame, fromCenter=False,
            showCrosshair=True)
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        print('initing')
        tracker1 = trackerFn()
        tracker1.init(frame, initBB1)
        tracker2 = trackerFn()
        tracker2.init(frame, initBB2)
        print('initialized')
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if key== ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()