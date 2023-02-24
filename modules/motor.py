import threading
import time
from adafruit_motorkit import MotorKit
import board

down = True
turning = [0] * 10

def execute_motor_instructions(motor_instruction, motor_id):
  global down
  count = 0
  while True:
    if len(motor_instruction) == 0:
      print(f"Motor {motor_id} Terminating")
      break
    if down and motor_instruction[0] == "0":
      motor_instruction = motor_instruction[1:]
      count += 1
      turn_motor(motor_id, "F")
      print(f"Motor {motor_id} turning..., Count: {count}, Motor Instruction: {motor_instruction}")
    elif not down and motor_instruction[0] == "1":
      motor_instruction = motor_instruction[1:]
      count += 1
      turn_motor(motor_id, "F")
      print(f"Motor {motor_id} turning..., Count: {count}, Motor Instruction: {motor_instruction}")


def send_motor_instructions(motor_instructions):
  global down, turning
  print(f"Motor Instructions: {motor_instructions}")

  for i in range(len(motor_instructions) // 6):
    # motor_t1 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6], 0))
    # motor_t2 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 1], 1))
    # motor_t3 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 2], 2))
    # motor_t4 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 3], 3))
    motor_t5 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 4], 8))
    motor_t6 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 5], 9))

    # motor_t1.start()
    # motor_t2.start()
    # motor_t3.start()
    # motor_t4.start()
    motor_t5.start()
    motor_t6.start()

  while (motor_t5.is_alive() or motor_t6.is_alive()):
    time.sleep(20)
    if down:
      print("Raising elevator")
      turn_motor(6, "F")
      down = False
    else:
      print("Lowering elevator")
      turn_motor(6, "B")
      down = True
  
  print("End")
  
def turn_motor(motor_id, direction="F"):
    global turning
    address = motor_id // 2 + 0x60
    
    print(turning)
    # Enable only 0x64 for testing purposes
    if address != 0x64:
        return
    turning[motor_id] = 1
    kit = MotorKit(address=address)
    print(f"Motor {motor_id} actually turning")
    for i in range(291):
        if (motor_id % 2 == 0):
            kit.stepper1.onestep()
        else:
            kit.stepper2.onestep()
    turning[motor_id] = 0
    print(f"Motor {motor_id} actually done turning")

if __name__ == "__main__":
  motor_instructions = ['001010', '001110', '011010', '011001', '000111', '111000']
  send_motor_instructions(motor_instructions)
  #turn_motor(8)
  #turn_motor(9)
