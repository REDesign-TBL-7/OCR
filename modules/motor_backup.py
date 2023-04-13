import time
import math
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

down = True
kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)
kit3 = MotorKit(address=0x62)
kit4 = MotorKit(address=0x63)

REVOLUTION = 2038
MOTOR_STEPS = 4
ELEVATOR_STEPS = 170
MOTOR_COUNT = 3

CONFIG_MAP = {
  '00': 0,
  '01': 1,
  '11': 2,
  '10': 3
}

def send_motor_instructions(motor_instructions):
  motor_steps = []
  for instruction in motor_instructions:
    motor_steps.append(CONFIG_MAP[instruction])

  turn_motors(motor_steps)
  turn_elevator_motor()
  time.sleep(5)
  turn_elevator_motor(direction=stepper.BACKWARD)
  

def turn_elevator_motor(direction=stepper.FORWARD, style=stepper.SINGLE):
  for i in range(ELEVATOR_STEPS):
    kit3.stepper2.onestep(direction=direction, style=style) # Edit elevator motors here
    kit3.stepper1.onestep(direction=direction, style=style)

def turn_motors(motor_steps):
  # motor_steps = [0, 1, 2] corresponding to the number of steps each motor has to turn
  while max(motor_steps) != 0:
    for i in range(REVOLUTION // MOTOR_STEPS):
      if motor_steps[0] > 0:
        kit1.stepper1.onestep()
      if motor_steps[1] > 0:
        kit1.stepper2.onestep()
      if motor_steps[2] > 0:
        kit2.stepper1.onestep()
    else:
      for i in range(len(motor_steps)):
        if motor_steps[i] > 0:
          motor_steps[i] -= 1
    


if __name__ == "__main__":
  motor_instructions = ['00', '01', '11']
  send_motor_instructions(motor_instructions)
  exit()