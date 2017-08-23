from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..track_objects_block import TrackObjects

from unittest.mock import patch, MagicMock
import sys


class TestTrackObjects(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['cv2'] = MagicMock()
        sys.modules['object_tracker'] = MagicMock()
        from ..track_objects_block import TrackObjects
        global TrackObjects

    def test_track_one_object(self):
        blk = TrackObjects()
        with patch(TrackObjects.__module__ + '.cv2.VideoCapture') as \
                mock_video_capture, \
                patch(TrackObjects.__module__ + '.object_tracker') as mock_face:
            mock_video_capture.return_value.read.return_value = \
                'bytes', 'frameBytes'
            self.configure_block(blk, {})
            blk.start()
            blk.process_signals([Signal({})])
            self.assert_num_signals_notified(1)
            self.assert_last_signal_list_notified([Signal({})])
            blk.stop()

    def test_track_two_objects(self):
        blk = TrackObjects()
        with patch(TrackObjects.__module__ + '.cv2.VideoCapture') as \
                mock_video_capture, \
                patch(TrackObjects.__module__ + '.object_tracker') as mock_face:
            mock_video_capture.return_value.read.return_value = \
                'bytes', 'frameBytes'
            self.configure_block(blk, {})
            blk.start()
            blk.process_signals([Signal({})])
            self.assert_num_signals_notified(1)
            self.assert_last_signal_list_notified([Signal({})])
            blk.stop()

    def track_none(self):
        blk = TrackObjects()
        with patch(TrackObjects.__module__ + '.cv2.VideoCapture') as \
                mock_video_capture, \
                patch(TrackObjects.__module__ + '.object_tracker') as mock_face:
            mock_video_capture.return_value.read.return_value = \
                'bytes', 'frameBytes'
            self.configure_block(blk, {})
            blk.start()
            blk.process_signals([Signal({})])
            self.assert_num_signals_notified(0)
            self.assert_last_signal_list_notified([Signal({})])
            blk.stop()
