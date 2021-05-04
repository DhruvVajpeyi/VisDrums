import numpy as np
import cv2


def get_circles(gray_frame):
    return cv2.HoughCircles(gray_frame, cv2.HOUGH_GRADIENT, 1.5, 25, param2=95)


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


cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    circles = get_circles(gray)
    circles2 = get_circles(gray2)
    draw_circles(circles, gray)
    draw_circles(circles2, gray2)

    # Display the resulting frame
    cv2.imshow('frame', gray)
    cv2.imshow('frame2', gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
