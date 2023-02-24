import cv2
import pytesseract
import numpy as np
from pytesseract import Output
from pybraille import convertText
import re
from gtts import gTTS
import os
from modules.motor import *

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
    ' ': '000000'}

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

if __name__ == "__main__":
    output_motor = ['001010', '001110', '011010', '011001', '110011', '101000']
    send_motor_instructions(output_motor)

    # Conversion to audio
    # language = 'en'
    # myobj = gTTS(text=output_string, lang=language, slow=False)
    # myobj.save("welcome.mp3")
    # os.system("mpg321 welcome.mp3")

    # Show image
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
