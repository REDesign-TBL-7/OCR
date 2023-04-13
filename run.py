from picamera import PiCamera
import cv2
import pytesseract
import numpy as np
from pytesseract import Output
from pybraille import convertText
import re
from gtts import gTTS
import os

BACKUP = True
# TODO: uncomment this later
# from modules.motor import *
# from modules.motor_backup import *
import time
import math
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from gpiozero import Button

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)
kit3 = MotorKit(address=0x62)
kit4 = MotorKit(address=0x63)

# Peripherals
PICTURE_PIN = 2
picture_button = Button(PICTURE_PIN)

NEXT_PIN = 3
next_button = Button(NEXT_PIN)

PREV_PIN = 4
prev_button = Button(PREV_PIN)

camera = PiCamera()

code_table = {
    'a': '100000',
    'b': '110000',
    'c': '100100',
    'd': '100110',
    'e': '100010',
    'f': '110100',
    'g': '110110',
    'h': '110010',
    'i': '010100',
    'j': '010110',
    'k': '101000',
    'l': '111000',
    'm': '101100',
    'n': '101110',
    'o': '101010',
    'p': '111100',
    'q': '111110',
    'r': '111010',
    's': '011100',
    't': '011110',
    'u': '101001',
    'v': '111001',
    'w': '010111',
    'x': '101101',
    'y': '101111',
    'z': '101011',
    '1': '100000',
    '2': '110000',
    '3': '100100',
    '4': '100110',
    '5': '100010',
    '6': '110100',
    '7': '110110',
    '8': '110010',
    '9': '010100',
    '0': '010110',
    ',': '010000',
    ';': '011000',
    ':': '010010',
    '.': '010011',
    '!': '011010',
    '(': '011011',
    ')': '011011',
    '?': '011001',
    '"': '011001',
    '*': '001010',
    '#': '001111',
    'Capital': '000001',
    'Letter': '000011',
    ' ': '000000'
}

output_braille = []
prev_state = ['000000', '000000', '000000']
pointer = 3

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

# removes all special characters and double spacing
def string_processing(string_input):
    pattern = r'[^A-Za-z0-9\\.\\*,;:!()"?\s]'
    string_input = re.sub(pattern, '', string_input)
    string_input = re.sub(" +", " ", string_input)
    return string_input

# converts string to a list of braille
def string_to_braille(string_input):
    letter_indicator = True
    braille_output = []
    for char in string_input:
        if (letter_indicator==True and char.isnumeric()):
            braille_output.append(code_table["Letter"])
            letter_indicator = False
        elif (letter_indicator==False and char.isalpha()):
            braille_output.append(code_table["#"])
            letter_indicator = True
        if (char.isupper()):
            braille_output.append(code_table['Capital'])
            char = char.lower()
        braille_output.append(code_table[char])
    return braille_output

def braille_to_motor(braille_input):
    motor_output = []
    for char in braille_input:
        if len(motor_output) == 0 or len(motor_output[-1]) == 6:
            motor_output.extend(["","",""])
        motor_output[-3] += char[:2]
        motor_output[-2] += char[2:4]
        motor_output[-1] += char[4:6]
    return motor_output

def capture_image_backup():
    print("Capturing Image...")

    camera.start_preview()
    camera.rotation = 180 # Depends how we eventually orientate the camera
    camera.capture("images/image.jpg")
    camera.stop_preview()

    # Read from camera
    img = cv2.imread("images/image.jpg")

    # Read from file
    # img = cv2.imread("images/1.jpg")

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['text'])

    output_string = ""
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # don't show empty text
            
            if text and text.strip() != "":
                output_string += text + " "
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                img = cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    print(f"String Output Bef: {output_string}")

    # String processing
    output_string = string_processing(output_string)
    print(f"String Output Aft: {output_string}")
    # print(f"String Output: {output_string}")

    # Conversion to list of braille
    output_braille = string_to_braille(output_string)
    print(f"Braille Output: {output_braille}")

    # Conversion to braille image
    # print(convertText(output_string))

    # Conversion to motor instructions
    pointer = 1

    # while pointer <= len(output_braille):
    output_motor = braille_to_motor(output_braille[pointer-1:pointer])

    print(f"Motor Output: {output_motor} | Batch: {pointer}")

    send_motor_instructions_backup(output_motor)

    # Save image
    cv2.imwrite('images/image_ocr.jpg', img)

def capture_image():
    global output_braille, pointer, prev_state

    print("Capturing Image...")

    camera.start_preview()
    camera.rotation = 180 # Depends how we eventually orientate the camera
    camera.capture("images/image.jpg")
    camera.stop_preview()

    # Read from camera
    img = cv2.imread("images/image.jpg")

    # Read from file
    # img = cv2.imread("images/1.jpg")

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['text'])

    output_string = ""
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # don't show empty text
            
            if text and text.strip() != "":
                output_string += text + " "
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                img = cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    print(f"String Output Bef: {output_string}")

    # String processing
    output_string = string_processing(output_string)
    print(f"String Output Aft: {output_string}")
    # print(f"String Output: {output_string}")

    # Conversion to list of braille
    output_braille = string_to_braille(output_string)
    print(f"Braille Output: {output_braille}")

    # Conversion to braille image
    # print(convertText(output_string))

    # Conversion to motor instructions
    pointer = 3
    prev_state = ['000000', '000000', '000000']
    # while pointer <= len(output_braille):
    curr_state = braille_to_motor(output_braille[pointer-3:pointer])

    output_motor = ["".join([str(int(a) ^ int(b)) for a, b in zip(x, y)]) for x, y in zip(curr_state, prev_state)]
    print(f"Motor Output: {output_motor} | Batch: {pointer // 3}")

    # send_motor_instructions(output_motor)
    prev_state = curr_state

    # Conversion to audio
    # language = 'en'
    # myobj = gTTS(text=output_string, lang=language, slow=False)
    # myobj.save("welcome.mp3")
    # os.system("mpg321 welcome.mp3")

    # Save image
    cv2.imwrite('images/image_ocr.jpg', img)

def next_chars():
    global pointer, output_braille, prev_state
    if pointer > len(output_braille):
        return
    elif pointer > len(output_braille) - 3:
        print("End of Output")
    pointer += 3
    curr_state = braille_to_motor(output_braille[pointer-3:pointer])
    output_motor = ["".join([str(int(a) ^ int(b)) for a, b in zip(x, y)]) for x, y in zip(curr_state, prev_state)]
    print(f"Motor Output: {output_motor} | Batch: {pointer // 3}")

    # send_motor_instructions(output_motor)
    prev_state = curr_state

def next_chars_backup():
    global output_braille, pointer
    if pointer > len(output_braille):
        return
    elif pointer > len(output_braille) - 1:
        print("End of Output")
    pointer += 1
    output_motor = braille_to_motor(output_braille[pointer-1:pointer])
    print(f"Motor Output: {output_motor} | Batch: {pointer}")

    send_motor_instructions_backup(output_motor)


def prev_chars():
    global pointer, output_braille, prev_state
    if pointer <= 3:
        return

    pointer -= 3
    curr_state = braille_to_motor(output_braille[pointer-3:pointer])
    output_motor = ["".join([str(int(a) ^ int(b)) for a, b in zip(x, y)]) for x, y in zip(curr_state, prev_state)]
    print(f"Motor Output: {output_motor} | Batch: {pointer // 3}")

    # send_motor_instructions(output_motor)
    prev_state = curr_state

def prev_chars_backup():
    global pointer, output_braille
    if pointer <= 1:
        return
    
    pointer -= 1
    output_motor = braille_to_motor(output_braille[pointer-1:pointer])
    print(f"Motor Output: {output_motor} | Batch: {pointer}")

    send_motor_instructions_backup(output_motor)

def send_motor_instructions_backup(motor_instructions):
  motor_steps = []
  for instruction in motor_instructions:
    motor_steps.append(CONFIG_MAP[instruction])

  print(f"Turning 5V Steppers... {motor_steps}")
  turn_motors(motor_steps.copy()) # Turn Motors

  print("Moving Up...")
  turn_elevator_motor()
  time.sleep(5)

  print("Moving Down...")
  turn_elevator_motor(direction=stepper.BACKWARD)
  time.sleep(5)

  print(f"Resetting Motors... {motor_steps}")
  turn_motors(motor_steps.copy(), direction=stepper.BACKWARD) # Reset Motors

def turn_elevator_motor(direction=stepper.FORWARD, style=stepper.SINGLE):
  for i in range(ELEVATOR_STEPS):
    kit3.stepper2.onestep(direction=direction, style=style) # Edit elevator motors here
    kit3.stepper1.onestep(direction=direction, style=style)

def turn_motors(motor_steps, direction=stepper.FORWARD):
  # motor_steps = [0, 1, 2] corresponding to the number of steps each motor has to turn

  while max(motor_steps) != 0:
    for i in range(REVOLUTION // MOTOR_STEPS):
      if motor_steps[0] > 0:
        kit1.stepper1.onestep(direction=direction)
      if motor_steps[1] > 0:
        kit1.stepper2.onestep(direction=direction)
      if motor_steps[2] > 0:
        kit2.stepper1.onestep(direction=direction)
    else:
      for i in range(len(motor_steps)):
        if motor_steps[i] > 0:
          motor_steps[i] -= 1

if __name__ == "__main__":
    print("Running program")

    picture_button.when_pressed = capture_image_backup if BACKUP else capture_image
    next_button.when_pressed = next_chars_backup if BACKUP else next_chars
    prev_button.when_pressed = prev_chars_backup if BACKUP else prev_chars

    while True:
        pass
