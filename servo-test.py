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
#  MA 02110-1301, USA.cd
#  
#  

from adafruit_servokit import ServoKit
from NerfTurret import NerfTurret
import time

plunger_in = 135
plunger_ext = 65

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range = (400, 2400)
kit.servo[1].set_pulse_width_range = (400, 2400)
kit.servo[2].set_pulse_width_range = (500, 2400)
kit.servo[0].actuation_range = 160
kit.servo[1].actuation_range = 160
kit.servo[2].actuation_range = 160

print("resetting angles")
kit.servo[0].angle = 90
kit.servo[1].angle = 90
kit.servo[2].angle = plunger_in
print("done... preparing firing")
time.sleep(1)

NerfTurret.fire()
#NerfTurret.fire()
"""
NerfTurret.fire()
NerfTurret.fire()
NerfTurret.fire()
NerfTurret.fire()
"""
"""
time.sleep(1)
for i in range(5):
	print("cycle", i)
	kit.servo[2].angle = plunger_in
	time.sleep(1)
	kit.servo[2].angle = plunger_ext
	time.sleep(1)
"""

"""
for i in range(5):
	print("cycle", i)
	kit.servo[0].angle = 45
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)

print("resetting")
kit.servo[0].angle = 0
"""
"""
kit.continuous_servo[0].throttle = 1
time.sleep(1)
kit.continuous_servo[0].throttle = -1
time.sleep(1)
kit.continuous_servo[0].throttle = 0
"""
"""
print("20")
kit.servo[0].angle = 20
time.sleep(1)
print("45")
kit.servo[0].angle = 45
time.sleep(1)
print("90")
kit.servo[0].angle = 90
time.sleep(1)
print("135")
kit.servo[0].angle = 135
time.sleep(1)
print("160")
kit.servo[1].angle = 160
time.sleep(0)
"""
