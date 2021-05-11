import numpy as np
import cv2


def get_circles(gray_frame):
    return cv2.HoughCircles(gray_frame, cv2.HOUGH_GRADIENT, 1.3, 50, param2=95)


def draw_circles(circles_list, img):
    if circles_list is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles_list = np.round(circles_list[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles_list:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(img, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
