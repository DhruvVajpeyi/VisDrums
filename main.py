import cv2
from circles import draw_circles, get_circles
from tracking import init_tracker, draw_bb, get_overlapped_circles

cap = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(0)

tracker_fn = cv2.TrackerCSRT_create
tracker1_top = None
tracker2_top = None

tracker1_side = None
tracker2_side = None

circles = None
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # ret2, frame2 = cap2.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    smoothed_gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
    # smoothed_gray2 = cv2.GaussianBlur(gray2, (7, 7), 1.5)

    smoothed_frame = cv2.GaussianBlur(frame, (7, 7), 1.5)
    # smoothed_frame2 = cv2.GaussianBlur(frame2, (7, 7), 1.5)

    if cv2.waitKey(1) & 0xFF == ord("w"):
        circles = get_circles(smoothed_gray)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1_top = init_tracker(smoothed_frame, "Tracker 1", tracker_fn)
        tracker2_top = init_tracker(smoothed_frame, "Tracker 2", tracker_fn)
        # tracker1_side = init_tracker(smoothed_frame2, "Tracker 1", tracker_fn)
        # tracker2_side = init_tracker(smoothed_frame2, "Tracker 2", tracker_fn)


    box1_top = draw_bb(tracker1_top, smoothed_frame)
    box2_top = draw_bb(tracker2_top, smoothed_frame)

    #box1_side = draw_bb(tracker1_side, smoothed_frame2)
    #box2_side = draw_bb(tracker2_side, smoothed_frame2)
    
    if circles is not None:
        draw_circles(circles, smoothed_frame)
        circle_idx1 = get_overlapped_circles(circles, box1_top)
        circle_idx2 = get_overlapped_circles(circles, box2_top)

        if (circle_idx1 != -1):
            print("Stick 1 overlapping: " + str(circle_idx1))
        if (circle_idx2 != -1):
            print("Stick 2 overlapping: " + str(circle_idx2))
    # Display the resulting frame
    cv2.imshow('frame', smoothed_frame)

    # cv2.imshow('frame2', gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
