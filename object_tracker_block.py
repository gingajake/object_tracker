from collections import deque
from enum import Enum
import numpy as np
import imutils
import cv2

from nio.block.base import Block, Signal
from nio.properties import Property, VersionProperty, ListProperty, \
    BoolProperty, PropertyHolder, SelectProperty, StringProperty, IntProperty


class FilterTypes(Enum):
    hsv = 'HSV'
    rgb = 'RGB'

class ImageFilters(PropertyHolder):
    filter_type = SelectProperty(FilterTypes,
                                 title='Filter type',
                                 default=FilterTypes.hsv)
    filter_lo = Property(title='Lower bounds for image filter',
                         default='',
                         allow_none=True)
    filter_hi = Property(title='Upper bounds for image filter',
                         default='',
                         allow_none=True)

class TrackObject(Block):

    version = VersionProperty('0.1.0')
    ipcam = BoolProperty(title='Use IP Camera?', default=False)
    camera = IntProperty(title='Camera Index', default=0)
    ipcam_address = StringProperty(title='IP Camera Address',
                                   default='',
                                   allow_none=True)
    video_ref = StringProperty(title='Path to video file',
                               default='',
                               allow_none=True)
    filters = ListProperty(ImageFilters,
                           title='Filters',
                           default=[])

    def __init__(self):
        super().__init__()
        self.video_capture = None

    def start(self):
        if not self.ipcam() and self.video_ref() == None:
            self.video_capture = cv2.VideoCapture(self.camera())
        else:
            self.video_capture = cv2.VideoCapture(self.video_ref())

    def process_signals(self, signals):
        counter = 0
        (dX, dY) = (0, 0)
        direction = ""

        for signal in signals:
            try:
                (grabbed,frame) = self.video_capture.read()
            except:
                break
            if (not grabbed):
                self.logger.critical('FAILED')
                break
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # construct a mask and perform dialations and erosions to remove
            # any small blobs left in the mask
            mask = cv2.inRange(hsv, tuple(self.filters()[0].filter_lo()),
                                tuple(self.filters()[0].filter_hi()))
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current center
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = (0,0)

            if len(cnts)>0:
        		# find the largest contour in the mask, then use to find centroid
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

            track_center = {
                'x_coord': center[0],
                'y_coord': center[1]
            }
            sig = Signal({
            "center" : track_center
            })

            self.notify_signals([sig])


# TODO: Support for multiple filters/objects
