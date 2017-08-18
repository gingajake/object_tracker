from nio.block.base import Block
from nio.properties import VersionProperty

from collections import deque
import numpy as np
import argparse
import imutils
import cv2

class FilterType(Enum):
    hsv = 'HSV'
    rgb = 'RGB'

class TrackObject(Block):

    version = VersionProperty('0.1.0')
    camera = IntProperty(title='Camera Index', default=0)
    ipcam = BoolProperty(title='Use IP Camera?', default=False)
    ipcam_address = StringProperty(title='IP Camera Address', default='')
    video_ref = StringProperty(title='Path to video file',default='')
    filter_type = SelectProperty(FilterType, title='Filter type',
                                 default=FilterType.hsv)
    filter_lo = StringProperty(title='Lower bounds for image filter',
                                default= (0, 0, 0))
    filter_hi = StringProperty(title='Upper bounds for image filter',
                                default= (255, 255, 255))

    def __init__(self):
        super().__init__()
        self.video_capture = None

    def start(self):
        if not self.ipcam():
            self.video_capture = cv2.VideoCapture(self.camera())

    def process_signals(self, signals):
        pts = deque(maxlen=args["buffer"])
        counter = 0
        (dX, dY) = (0, 0)
        direction = ""

        for signal in signals:
            (grabbed,frame) = camera.read()
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # construct a mask and perform dialations and erosions to remove
            # any small blobs left in the mask
            mask = cv2.inRange(hsv, redCarLower, redCarUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            # only proceed if at least one contour was found
        	if len(cnts) > 0:
        		# find the largest contour in the mask, then use to compute centroid
        		c = max(cnts, key=cv2.contourArea)
        		((x, y), radius) = cv2.minEnclosingCircle(c)
        		M = cv2.moments(c)
        		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        		# only proceed if the radius meets a minimum size
        		if radius > 10:
        			# draw the circle and centroid on the frame & update points
        			cv2.circle(frame, (int(x), int(y)), int(radius),
        				(0, 255, 255), 2)
        			cv2.circle(frame, center, 5, (0, 0, 255), -1)

        	# update the points queue
        	pts.appendleft(center)
        	# loop over the set of tracked points
        	for i in range(1, len(pts)):
        		# if either of the tracked points are None, ignore
        		# them
        		if pts[i - 1] is None or pts[i] is None:
        			continue

        		# otherwise, compute the thickness of the line and
        		# draw the connecting lines
        		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        	# show the frame to our screen
        	cv2.imshow("Frame", frame)
        	key = cv2.waitKey(1) & 0xFF

             sig = Signal({
                #NEED JAMES TO LET ME KNOW WHATS NEEDED
            })
            self.notify_signals([sig])

        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
