import cv2
from circles import draw_circles, get_circles
from tracking import init_tracker, draw_bb, get_overlapped_circles, check_if_below_line, check_if_reset_line
import playsound

line_threshold = 150

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

tracker_fn = cv2.TrackerCSRT_create
tracker1_top = None
tracker2_top = None

tracker1_side = None
tracker2_side = None

line = None

below_line_1 = False
below_line_2 = False
reset_hit_1 = True
reset_hit_2 = True

circles = None
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    smoothed_gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
    smoothed_gray2 = cv2.GaussianBlur(gray2, (7, 7), 1.5)

    smoothed_frame = cv2.GaussianBlur(frame, (7, 7), 1.5)
    smoothed_frame2 = cv2.GaussianBlur(frame2, (7, 7), 1.5)

    if cv2.waitKey(1) & 0xFF == ord("c"):
        circles = get_circles(gray)

    if cv2.waitKey(1) & 0xFF == ord("t"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1_top = init_tracker(smoothed_gray, "Tracker 1", tracker_fn)
        tracker2_top = init_tracker(smoothed_gray, "Tracker 2", tracker_fn)
    if cv2.waitKey(1) & 0xFF == ord("s"):
        tracker1_side = init_tracker(smoothed_gray2, "Tracker 3", tracker_fn)
        tracker2_side = init_tracker(smoothed_gray2, "Tracker 4", tracker_fn)

    box1_top = draw_bb(tracker1_top, smoothed_frame)
    box2_top = draw_bb(tracker2_top, smoothed_frame)

    box1_side = draw_bb(tracker1_side, smoothed_frame2)
    box2_side = draw_bb(tracker2_side, smoothed_frame2)

    if circles is not None:
        draw_circles(circles, smoothed_frame)
        circle_idx1 = get_overlapped_circles(circles, box1_top)
        circle_idx2 = get_overlapped_circles(circles, box2_top)

        if circle_idx1 != -1 and below_line_1 and reset_hit_1:
            print("Stick 1 overlapping: " + str(circle_idx1))
            playsound.playsound("samples/bass.wav", block=False)
            reset_hit_1 = False
        if circle_idx2 != -1 and below_line_2 and reset_hit_2:
            print("Stick 2 overlapping: " + str(circle_idx2))
            playsound.playsound("samples/bass.wav", block=False)
            reset_hit_2 = False

    line = cv2.line(smoothed_frame2, (0, smoothed_frame2.shape[0] - line_threshold),
                    (smoothed_frame2.shape[1], smoothed_frame2.shape[0] - line_threshold), (0, 0, 255),
                    7)
    below_line_1 = check_if_below_line(smoothed_frame2.shape[0] - line_threshold, box1_side)
    below_line_2 = check_if_below_line(smoothed_frame2.shape[0] - line_threshold, box2_side)
    reset_hit_1 = check_if_reset_line(smoothed_frame2.shape[0] - line_threshold, box1_side, reset_hit_1)
    reset_hit_2 = check_if_reset_line(smoothed_frame2.shape[0] - line_threshold, box2_side, reset_hit_2)

    # Display the resulting frame
    cv2.imshow('frame', smoothed_frame)
    cv2.imshow('frame2', smoothed_frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
