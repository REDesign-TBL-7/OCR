# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
from adafruit_motorkit import MotorKit


kit4 = MotorKit(address=0x63)

while True:
  kit4.motor1.throttle = 1.0
  kit4.motor2.throttle = 1.0
  time.sleep(0.5)
  kit4.motor1.throttle = 0
  kit4.motor2.throttle = 0
