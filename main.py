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

sounds = ["samples/bass.wav", "samples/hat.wav", "samples/snare.wav"]
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    #smoothed_frame = cv2.GaussianBlur(frame, (7, 7), 1.5)
    #smoothed_frame2 = cv2.GaussianBlur(frame2, (7, 7), 1.5)

    if cv2.waitKey(1) & 0xFF == ord("c"):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        smoothed_gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
        circles = get_circles(smoothed_gray)

    if cv2.waitKey(1) & 0xFF == ord("t"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        tracker1_top = init_tracker(frame, "Tracker 1", tracker_fn)
        tracker2_top = init_tracker(frame, "Tracker 2", tracker_fn)
    if cv2.waitKey(1) & 0xFF == ord("s"):
        tracker1_side = init_tracker(frame2, "Tracker 3", tracker_fn)
        tracker2_side = init_tracker(frame2, "Tracker 4", tracker_fn)

    box1_top = draw_bb(tracker1_top, frame)
    box2_top = draw_bb(tracker2_top, frame)

    box1_side = draw_bb(tracker1_side, frame2)
    box2_side = draw_bb(tracker2_side, frame2)

    below_line_1 = check_if_below_line(frame2.shape[0] - line_threshold, box1_side)
    below_line_2 = check_if_below_line(frame2.shape[0] - line_threshold, box2_side)
    reset_hit_1 = check_if_reset_line(frame2.shape[0] - line_threshold, box1_side, reset_hit_1)
    reset_hit_2 = check_if_reset_line(frame2.shape[0] - line_threshold, box2_side, reset_hit_2)
    
    if circles is not None:
        draw_circles(circles, frame)
        circle_idx1 = get_overlapped_circles(circles, box1_top)
        circle_idx2 = get_overlapped_circles(circles, box2_top)

        if circle_idx1 != -1 and below_line_1 and reset_hit_1:
            print("Stick 1 overlapping: " + str(circle_idx1))
            playsound.playsound(sounds[circle_idx1], block=False)
            reset_hit_1 = False
        if circle_idx2 != -1 and below_line_2 and reset_hit_2:
            print("Stick 2 overlapping: " + str(circle_idx2))
            playsound.playsound(sounds[circle_idx2], block=False)
            reset_hit_2 = False


    line = cv2.line(frame2, (0, frame2.shape[0] - line_threshold),
                    (frame2.shape[1], frame2.shape[0] - line_threshold), (0, 0, 255),
                    7)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('frame2', frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
