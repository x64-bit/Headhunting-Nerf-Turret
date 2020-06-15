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

# TODO: refactor servo ids to represent servo objects themselves

from adafruit_servokit import ServoKit
import time
import sys
import RPi.GPIO as GPIO

# GPIO outputs for flywheel operation
pin_forward = 26
pin_backward = 20

# GPIO setup
mode=GPIO.getmode()
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_forward, GPIO.OUT)
GPIO.setup(pin_backward, GPIO.OUT)

# servo ids
servo_pan = 0
servo_tilt = 1 # may or may not be possible.
servo_fire = 2
kit = ServoKit(channels=16)
kit.actuation_range = 160
is_aiming = False

# reference servo angles for cycling darts
plunger_in = 135
plunger_ext = 65

class NerfTurret:
	
	# note to self: classmethods = static methods that can also be used
	# as an instance method.
	@classmethod
	def aim(self, angle_x):
		is_aiming = True
		print("aiming")
		kit.servo[servo_pan].angle = angle_x
		is_aiming = False
	
	@classmethod
	def fire(self):
		print("firing")
		kit.servo[servo_fire].angle = plunger_in
		GPIO.output(pin_forward, GPIO.HIGH)
		time.sleep(1.5)
		kit.servo[servo_fire].angle = plunger_ext
		time.sleep(0.75)
		GPIO.output(pin_forward, GPIO.LOW)
		kit.servo[servo_fire].angle = plunger_in
		
	@classmethod
	def resetAngle(self):
		print("resetting")
		kit.servo[servo_pan].angle = 90
		kit.servo[servo_fire].angle = plunger_in
	
	@classmethod
	def currentlyAiming(self):
		print("Aiming status: ", is_aiming)
		return is_aiming
		
