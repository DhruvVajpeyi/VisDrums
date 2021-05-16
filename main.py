import cv2
from circles import draw_circles, get_circles
from tracking import init_tracker, draw_bb, get_overlapped_circles, check_if_below_line, check_if_reset_line
from multiprocessing import Process, Value
import pygame

def top_view(circle_idx1, circle_idx2):
    cap = cv2.VideoCapture(0)
    tracker1_top = None
    tracker2_top = None
    circles = None
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        #smoothed_frame = cv2.GaussianBlur(frame, (7, 7), 1.5)
        #smoothed_frame2 = cv2.GaussianBlur(frame2, (7, 7), 1.5)
        key = cv2.waitKey(1)
        if key & 0xFF == ord("c"):
            print("calibrate circles")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            smoothed_gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
            circles = get_circles(smoothed_gray)
            print(circles)
        elif key & 0xFF == ord("t"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            tracker1_top = init_tracker(frame, "Tracker 1")
            tracker2_top = init_tracker(frame, "Tracker 2")
        elif key & 0xFF == ord('q'):
            break
    
        box1_top = draw_bb(tracker1_top, frame)
        box2_top = draw_bb(tracker2_top, frame)
    
        if circles is not None:
            circle_idx1.value = get_overlapped_circles(circles, box1_top)
            circle_idx2.value = get_overlapped_circles(circles, box2_top)

        draw_circles(circles, frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
    cap.release()
    cv2.destroyAllWindows()

def side_view(circle_idx1, circle_idx2):
    cap = cv2.VideoCapture(1)
    tracker1_side = None
    tracker2_side = None

    line_threshold = 150

    below_line_1 = False
    below_line_2 = False
    reset_hit_1 = True
    reset_hit_2 = True

    pygame.mixer.init()
    sounds = [pygame.mixer.Sound("samples/bass.wav"), pygame.mixer.Sound("samples/snare.wav"), pygame.mixer.Sound("samples/hat.wav")]
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        #smoothed_frame = cv2.GaussianBlur(frame, (7, 7), 1.5)
        #smoothed_frame2 = cv2.GaussianBlur(frame2, (7, 7), 1.5)
        key = cv2.waitKey(1)
        if key & 0xFF == ord("s"):
            tracker1_side = init_tracker(frame, "Tracker 3")
            tracker2_side = init_tracker(frame, "Tracker 4")
        elif key & 0xFF == ord('q'):
            break
    
        box1_side = draw_bb(tracker1_side, frame)
        box2_side = draw_bb(tracker2_side, frame)

        below_line_1 = check_if_below_line(frame.shape[0] - line_threshold, box1_side)
        below_line_2 = check_if_below_line(frame.shape[0] - line_threshold, box2_side)
        reset_hit_1 = check_if_reset_line(frame.shape[0] - line_threshold, box1_side, reset_hit_1)
        reset_hit_2 = check_if_reset_line(frame.shape[0] - line_threshold, box2_side, reset_hit_2)
    
        if circle_idx1.value != -1 and below_line_1 and reset_hit_1:
            sounds[circle_idx1.value].play()
            reset_hit_1 = False
        if circle_idx2.value != -1 and below_line_2 and reset_hit_2:
            sounds[circle_idx2.value].play()
            reset_hit_2 = False

        cv2.line(frame, (0, frame.shape[0] - line_threshold),
                    (frame.shape[1], frame.shape[0] - line_threshold), (0, 0, 255),
                    7)

        # Display the resulting frame
        cv2.imshow('frame2', frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    circle_idx1 = Value('i', -1)
    circle_idx2 = Value('i', -1)

    top_cam = Process(target=top_view, args=(circle_idx1, circle_idx2))
    side_cam = Process(target=side_view, args=(circle_idx1, circle_idx2))
    top_cam.start()
    side_cam.start()
    top_cam.join()
    side_cam.join()