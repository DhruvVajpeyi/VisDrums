import cv2
from circles import draw_circles, get_circles
from tracking import init_tracker, draw_bb

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)

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

    circles = get_circles(gray)
    # circles2 = get_circles(gray2)
    draw_circles(circles, gray)
    # draw_circles(circles2, gray2)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1 = init_tracker(gray, "Tracker 1", tracker_fn)
        tracker2 = init_tracker(gray, "Tracker 2", tracker_fn)

    draw_bb(tracker1, gray, circles)
    draw_bb(tracker2, gray, circles)

    # Display the resulting frame
    cv2.imshow('frame', gray)

    # cv2.imshow('frame2', gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
