import threading
import time

down = True
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
      print(f"Motor {motor_id} turning..., Count: {count}, Motor Instruction: {motor_instruction}")
      time.sleep(1)
    elif not down and motor_instruction[0] == "1":
      motor_instruction = motor_instruction[1:]
      count += 1
      print(f"Motor {motor_id} turning..., Count: {count}, Motor Instruction: {motor_instruction}")
      time.sleep(1)


def send_motor_instructions(motor_instructions):
  global down
  print(f"Motor Instructions: {motor_instructions}")

  for i in range(len(motor_instructions) // 6):
    motor_t1 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6], 1))
    motor_t2 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 1], 2))
    motor_t3 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 2], 3))
    motor_t4 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 3], 4))
    motor_t5 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 4], 5))
    motor_t6 = threading.Thread(target=execute_motor_instructions, args=(motor_instructions[i * 6 + 5], 6))

    motor_t1.start()
    motor_t2.start()
    motor_t3.start()
    motor_t4.start()
    motor_t5.start()
    motor_t6.start()

  while motor_t1.is_alive() or motor_t2.is_alive() or motor_t3.is_alive() or motor_t4.is_alive():
    time.sleep(6)
    if down:
      print("Raising elevator")
      down = False
    else:
      print("Lowering elevator")
      down = True
  
  print("End")

if __name__ == "__main__":
  motor_instructions = ['001010', '001110', '011010', '011001', '110011', '101000']
  send_motor_instructions(motor_instructions)
