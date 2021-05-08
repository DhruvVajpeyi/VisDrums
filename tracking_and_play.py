from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

import pyaudio  
import wave

bass_path = "./samples/bass.wav"
hat_path = "./samples/hat.wav"
snare_path = "./samples/snare.wav"

def play_audio_callback(wave_path):
	# define stream chunk 
	CHUNK = 1024
	# open a wav format music
	wf = wave.open(wave_path, 'rb')
	# instantiate PyAudio (1)
	p = pyaudio.PyAudio()
	def callback(in_data, frame_count, time_info, status):
		data = wf.readframes(frame_count)
		return (data, pyaudio.paContinue)
	# open stream (2)
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
		channels=wf.getnchannels(),
		rate=wf.getframerate(),
		output=True,
		stream_callback=callback)
	# read data
	stream.start_stream()
	while stream.is_active():
		time.sleep(0.1)
	# stop stream (4)
	stream.stop_stream()
	stream.close()
	# close PyAudio (5)
	p.terminate()

def intersection(a, b, r, x, y, w, h):
    o1 = np.array([x + w / 2, y + w / 2])
    o2 = np.array([a, b])
    v = abs(o1 - o2)
    h = np.array([x + w, y + h]) - o1
    u = np.maximum(v - h, 0)
    return np.dot(u, u) <= r ** 2

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.legacy.TrackerCSRT_create,
	"kcf": cv2.legacy.TrackerKCF_create,
	"boosting": cv2.legacy.TrackerBoosting_create,
	"mil": cv2.legacy.TrackerMIL_create,
	"tld": cv2.legacy.TrackerTLD_create,
	"medianflow": cv2.legacy.TrackerMedianFlow_create,
	"mosse": cv2.legacy.TrackerMOSSE_create
}

trackers = cv2.legacy.MultiTracker_create()

cap = cv2.VideoCapture(0)
# initialize the FPS throughput estimator
fps = None
prevboxes = None

# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	ret, frame = cap.read()
	# check to see if we have reached the end of the stream
	if frame is None:
		break
	# resize the frame (so we can process it faster) and grab the
	# frame dimensions
	frame = imutils.resize(frame, width=1000)
	(H, W) = frame.shape[:2]

	# grab the new bounding box coordinates of the object
	(success, boxes) = trackers.update(frame)
	
	if not success:
		trackers = cv2.legacy.MultiTracker_create()

	# check to see if the tracking was a success
	if success and len(boxes) > 0:
		for i in range(len(boxes)):
			(x, y, w, h) = [int(v) for v in boxes[i]]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)

			if intersection(800, 281, 150, x, y, w, h):
				print("True")

				if prevboxes is not None and len(prevboxes) >= 1:
					b1 = (x, y, x + w, y + h)
					xp, yp, wp, hp = [int(v) for v in prevboxes[i]]
					b2 = (xp, yp, xp + wp, yp + hp)
					# bounding box intersection over union
					if bb_intersection_over_union(b1, b2) < 0.7:

						play_audio_callback(bass_path)

		# update the FPS counter
		fps.update()
		fps.stop()
		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("Tracker", args["tracker"]),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	prevboxes = boxes

	a = cv2.circle(frame, (200, 281), 150, (0, 255, 0), 2)
	b = cv2.circle(frame, (500, 281), 150, (0, 255, 0), 2)
	c = cv2.circle(frame, (800, 281), 150, (0, 255, 0), 2)

	# show the output frame
	cv2.imshow("Vision-Based Drum Input", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		box = cv2.selectROI("Vision-Based Drum Input", frame, fromCenter=False,
			showCrosshair=True)
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		if box != (0, 0, 0, 0):
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)
			fps = FPS().start()
			# play_bass(f)
	elif key == ord("a"):
		play_audio_callback(bass_path)
	elif key == ord("l"):
		play_audio_callback(snare_path)
	elif key == ord(" "):
		play_audio_callback(hat_path)
	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

cap.release()
# close all windows
cv2.destroyAllWindows()
