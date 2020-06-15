#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2020  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

from NerfTurret import NerfTurret
from FaceTracker import FaceTracker

import time
import math
import numpy as np

res_x, res_y = 640, 480

camera = PiCamera()
camera.resolution = (res_x, res_y)
camera.framerate = 60
camera.exposure_mode = "night"
camera.rotation = 270
fov = 53.5 * math.pi/180
raw_capture = PiRGBArray(camera, size=(res_x,res_y))
face_tracker = FaceTracker(res_x, res_y, fov)

# warm up camera
time.sleep(0.2)


def main(args):
    """
    Runs the turret
    """
    start_time = time.time()
    # buffer time for aiming
    buffer_time = time.time()
    
    NerfTurret.resetAngle()
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        face_detected, angle_x, angle_y = face_tracker.findCoords(image)
        
        if time.time() - start_time > 5: # leave some warmup time
            if face_detected:
                print("angle:", angle_x)
                NerfTurret.aim(angle_x)
                # maybe create method for revving flywheel
                # if NerfTurret.fire() too slow
                if time.time() - buffer_time > .5:
                    print("FIRE!!")
                    NerfTurret.fire()
                    buffer_time = time.time()
            else:
                print("Searching...")
        else:
            print("Warming up...")
        
        # display images
        cv2.imshow("Faces", image)
        raw_capture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
    
    NerfTurret.resetAngle()
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
