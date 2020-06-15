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

import math
import cv2
import imutils
import numpy as np

class FaceTracker:
	
	def __init__(self, x, y, fov):
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		self.res_x = x
		self.res_y = y
		self.fov = fov

	def aimCoordinateConverter(self, res_x, res_y, pos_x, pos_y):
		"""
		Converts coordinates to range of [-1, 1]
		"""
		norm_x = (pos_x - 0.5 * res_x)/(res_x/2)
		norm_y = (pos_y - 0.5 * res_y)/(res_y/2)
		
		return norm_x, -norm_y
    
	def calculateTargetAngle(self, coord):
		"""
		Painful trig to find servo turn angle
		"""
		# servo is centered at 90. add calculated turn angle, clip to
		# [20, 160] to make sure that servo doesn't blow itself up.
		return math.atan(math.tan(self.fov/2) * coord) * 180/math.pi

	def findCoords(self, image):
		"""
		Find the coordinates/angle of an image
		"""
		face_detected = False
		pos_x = pos_y = angle_x = angle_y = None
		
		faces = self.face_cascade.detectMultiScale(image, 1.3, 5)
		
		for (x,y,w,h) in faces:
			face_detected = True
			print("Target detected. Aiming...")
			pos_x, pos_y = self.aimCoordinateConverter(self.res_x, self.res_y, x+(w/2), y+(h/2))
			angle_x = np.clip(90 - self.calculateTargetAngle(pos_x), 20, 160)
			angle_y = np.clip(90 + self.calculateTargetAngle(pos_y), 20, 160)
			
			# print("Coordinates: {0}, {1}".format(pos_x, pos_y))
			print("Angle calculated: x={0}, y={1}".format(angle_x, angle_y))
			
			image = cv2.rectangle(image, (x,y), (x+w, y+h), (40, 40, 178), 2)
			cv2.putText(image, "!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (40, 40, 178), 2)
			
			break
		
		return face_detected, angle_x, angle_y
