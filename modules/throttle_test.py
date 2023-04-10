# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
from adafruit_motorkit import MotorKit

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)
kit3 = MotorKit(address=0x62)
kit4 = MotorKit(address=0x63)

while True:
  kit1.stepper1.throttle = 1
  kit1.stepper2.throttle = 1
  kit2.stepper1.throttle = 1
  kit2.stepper2.throttle = 1
  kit3.stepper1.throttle = 1
  kit3.stepper2.throttle = 1
  kit4.stepper1.throttle = 1
  kit4.stepper2.throttle = 1
  time.sleep(1)
