import cv2
from circles import draw_circles, get_circles
from tracking import init_tracker, draw_bb, get_overlapped_circles, check_if_below_line, check_if_reset_line
from multiprocessing import Process, Value
import pygame
from time import perf_counter

""" The main loop for the top view camera, and circle bound detection
args: circle_idx1, circle_idx2 : Global values from multiprocessing.Value. Used to share the detected circle overlap with the hit detection process
"""
def top_view(circle_idx1, circle_idx2):
    # Begin capture of Cam 1 (The top view)
    cap = cv2.VideoCapture(0)

    # Initialize trackers for each stick
    tracker1_top = None
    tracker2_top = None

    # Initialize detected circles
    circles = None

    # Initialize performance trackers
    pre_time = perf_counter()
    frames = 0
    fps = "0"

    # Main Loop
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Preprocess the frame with gaussian blurring
        frame = cv2.GaussianBlur(frame, (7, 7), 1.5)

        # Keystroke handler
        key = cv2.waitKey(1)
        if key & 0xFF == ord("c"):
            # Detect circles on keystroke "c"
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #cv2 HoughCircles requires grayscale image
            smoothed_gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
            circles = get_circles(smoothed_gray)
        elif key & 0xFF == ord("t"):
            # select the bounding box of the object we want to track
            tracker1_top = init_tracker(frame, "Tracker 1")
            tracker2_top = init_tracker(frame, "Tracker 2")
        elif key & 0xFF == ord('q'):
            break
    
        # Get updated bounding boxes
        box1_top = draw_bb(tracker1_top, frame)
        box2_top = draw_bb(tracker2_top, frame)
    
        # Detect overlapped circle for each stick
        if circles is not None:
            circle_idx1.value = get_overlapped_circles(circles, box1_top)
            circle_idx2.value = get_overlapped_circles(circles, box2_top)

        # Update frame with drawn circles and performance metrics
        draw_circles(circles, frame)
        update_time = perf_counter()

        # Update FPS every second
        if(update_time - pre_time >= 1):
            fps = "{:.2f}".format(frames/(update_time-pre_time))
            pre_time = update_time
            frames = 0
        frame = cv2.putText(frame, 'FPS: ' + fps, (0, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 0, 0))

        # Display the resulting frame
        cv2.imshow('frame', frame)
        frames += 1
    cap.release()
    cv2.destroyAllWindows()

""" The main loop for the side view camera, and hit detection
args: circle_idx1, circle_idx2 : Global values from multiprocessing.Value. Used to share the detected circle overlap with the hit detection process
"""
def side_view(circle_idx1, circle_idx2):
    # Begin capture of Cam 2 (The side view)
    cap = cv2.VideoCapture(1)

    # Initialize trackers for each stick
    tracker1_side = None
    tracker2_side = None

    # Declare the hit detection line
    line_threshold = 150

    # Initialize stick position above hit line
    reset_hit_1 = True
    reset_hit_2 = True

    # Initialize performance metrics
    pre_time = perf_counter()
    frames = 0
    fps = "0"
    hits = 0
    bpm = "0"

    # Initialize audio mixer
    pygame.mixer.init()
    sounds = [pygame.mixer.Sound("samples/bass.wav"), pygame.mixer.Sound("samples/snare.wav"), pygame.mixer.Sound("samples/hat.wav")]

    # Main loop
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Preprocess the frame with gaussian blurring
        frame = cv2.GaussianBlur(frame, (7, 7), 1.5)

        # Keystroke handler
        key = cv2.waitKey(1)
        if key & 0xFF == ord("s"):
            # select the bounding box of the object we want to track. Must be same order as top view
            tracker1_side = init_tracker(frame, "Tracker 3")
            tracker2_side = init_tracker(frame, "Tracker 4")
        elif key & 0xFF == ord('q'):
            break
    
        # Get updated bounding boxes
        box1_side = draw_bb(tracker1_side, frame)
        box2_side = draw_bb(tracker2_side, frame)

        # Check if bounding box has passed hit line downwards
        below_line_1 = check_if_below_line(frame.shape[0] - line_threshold, box1_side)
        below_line_2 = check_if_below_line(frame.shape[0] - line_threshold, box2_side)
        reset_hit_1 = check_if_reset_line(frame.shape[0] - line_threshold, box1_side, reset_hit_1)
        reset_hit_2 = check_if_reset_line(frame.shape[0] - line_threshold, box2_side, reset_hit_2)
    
        # Hit detection for stick 1. Circle_idx is set by top view process
        if circle_idx1.value != -1 and below_line_1 and reset_hit_1:
            sounds[circle_idx1.value].play()
            reset_hit_1 = False
            hits += 1
        # Hit detection for stick 2
        if circle_idx2.value != -1 and below_line_2 and reset_hit_2:
            sounds[circle_idx2.value].play()
            reset_hit_2 = False
            hits += 1

        # Draw hit line on frame
        cv2.line(frame, (0, frame.shape[0] - line_threshold),
                    (frame.shape[1], frame.shape[0] - line_threshold), (0, 0, 255),
                    7)

        update_time = perf_counter()

        #Update FPS and BPM every second
        if(update_time - pre_time >= 1):
            fps = "{:.2f}".format(frames/(update_time-pre_time))
            bpm = "{:.2f}".format(60*hits/(update_time-pre_time))
            pre_time = update_time
            frames = 0
            hits = 0

        frame = cv2.putText(frame, 'FPS: ' + fps, (frame.shape[0]-50, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 0, 0))
        frame = cv2.putText(frame, 'BPM: ' + bpm, (frame.shape[0]-50, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 0, 0))

        # Display the resulting frame
        cv2.imshow('frame2', frame)
        frames += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    circle_idx1 = Value('i', -1)
    circle_idx2 = Value('i', -1)

    # Start 2 separate processes. One for each camera. Share the overlapped circle indices. 
    top_cam = Process(target=top_view, args=(circle_idx1, circle_idx2))
    side_cam = Process(target=side_view, args=(circle_idx1, circle_idx2))
    top_cam.start()
    side_cam.start()
    top_cam.join()
    side_cam.join()