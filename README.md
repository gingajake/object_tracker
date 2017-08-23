TrackObject
========
Grab a frame of video from a specified camera, find an object based on filtering
defined in the block, and then output the centroid location of that object.

Properties
----------
- **camera**: Where to find the local camera to read from.
- **frame_size**: Scaling factor for frame.
- **camera**: Whether or not to use an IP Camera.
- **ipcam**: Whether or not to use an IP Camera.
- **ipcam_address**: Address for where to find the IP camera.
- **video_ref**: File location of video to be processed
- **filters**: List of filters used for image processing and tracking
- **obj**: Name of object to be tracked, characterized by filter type and bands
- **filter_type**: HSV or RGB filter for defining the mask
- **filter_lo**: Low band of filter
- **filter_hi**: High band of filter


Inputs
------

Outputs
-------
- **track**: A signal containing the object and it's reference coordinates in the frame.

Commands
--------

Dependencies
------------
-    opencv-python
-    argparse
-    imutils
-    numpy

Input Example
-------------
```
```

Output Example
--------------
```
{
 'object': 'TestObject',
 'x_coord': 123,
 'y_coord': 456
}
```
