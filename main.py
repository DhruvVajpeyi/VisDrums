import cv2
from circles import draw_circles, get_circles
from tracking import init_tracker, draw_bb, get_overlapped_circles

cap = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(0)

tracker_fn = cv2.TrackerCSRT_create
tracker1 = None
tracker2 = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # ret2, frame2 = cap2.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    smoothed = cv2.GaussianBlur(gray, (7, 7), 1.5)

    circles = get_circles(smoothed)
    # circles2 = get_circles(gray2)
    
    # draw_circles(circles2, gray2)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1 = init_tracker(smoothed, "Tracker 1", tracker_fn)
        tracker2 = init_tracker(smoothed, "Tracker 2", tracker_fn)

    box1 = draw_bb(tracker1, smoothed)
    box2 = draw_bb(tracker2, smoothed)

    draw_circles(circles, smoothed)
    circle_idx1 = get_overlapped_circles(circles, box1)
    circle_idx2 = get_overlapped_circles(circles, box2)

    if (circle_idx1 != -1):
        print("Stick 1 overlapping: " + str(circle_idx1))
    if (circle_idx2 != -1):
        print("Stick 2 overlapping: " + str(circle_idx2))
    # Display the resulting frame
    cv2.imshow('frame', smoothed)

    # cv2.imshow('frame2', gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
