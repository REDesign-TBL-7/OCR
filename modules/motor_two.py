import threading
import time
from adafruit_motorkit import MotorKit
import board

down = True
kit1 = MotorKit(address=0x60)
# kit2 = MotorKit(address=0x61)
# kit3 = MotorKit(address=0x62)
# kit4 = MotorKit(address=0x63)

def send_motor_instructions(motor_instructions):
  global down
  print(f"Motor Instructions: {motor_instructions}")

  motors_executed_count = 0
  while motors_executed_count != 6:
    print(motor_instructions)
    motors_done_count = 0
    while motors_done_count != 6:
      motors_done_count = 0
      motors_to_turn = {
        0: False,
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False
      }
      for i in range(len(motor_instructions)):
        motor_instruction = motor_instructions[i]
        if motor_instruction == "" or down and motor_instruction[0] == "1" or not down and motor_instruction[0] == "0":
          motors_done_count += 1
          continue
        if down and motor_instruction[0] == "0":
          motors_to_turn[i] = True
          motor_instructions[i] = motor_instruction[1:]
        if not down and motor_instruction[0] == "1":
          motors_to_turn[i] = True
          motor_instructions[i] = motor_instruction[1:]
        if motor_instructions[i] == "":
          motors_executed_count += 1

      turn_motors(motors_to_turn)

    if down:
      print("Raising elevator")
      turn_elevator_motor()
      down = False
    else:
      print("Lowering elevator")
      turn_elevator_motor(direction="B")
      down = True

  print("End")
  exit()

def turn_elevator_motor(direction="F"):
  for i in range(291):
#    kit4.stepper1.onestep(direction=direction)
    pass

def turn_motors(motor_ids):
  for i in range(291):
    if (motor_ids[0]):
      kit1.stepper1.onestep()
    if (motor_ids[1]):
      kit1.stepper2.onestep()
#    if (motor_ids[2]):
#      kit2.stepper1.onestep()
#    if (motor_ids[3]):
#      kit2.stepper2.onestep()
#    if (motor_ids[4]):
#      kit3.stepper1.onestep()
#    if (motor_ids[5]):
#      kit3.stepper2.onestep()

if __name__ == "__main__":
  motor_instructions = ['001010', '001110', '011010', '011001', '000111', '111000']
  send_motor_instructions(motor_instructions)
