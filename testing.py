import cv2
import pytesseract
import numpy as np
from pytesseract import Output
from pybraille import convertText
import re

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

img =cv2.imread('IMG_9082.PNG')

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
output_string = string_processing(output_string)
output_string = output_string[:5]
print(output_string)
output_braille = string_to_braille(output_string)
print(output_braille)
print(convertText(output_string))

cv2.imshow('img', img)
cv2.waitKey(0)

#hello world