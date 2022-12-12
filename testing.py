import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import re

# removes all special characters and double spacing
def string_processing(string_input):
    pattern = r'[^A-Za-z0-9\\.\\*,;:!()"?\s]'
    string_input = re.sub(pattern, '', string_input)
    string_input = re.sub(" +", " ", string_input)
    return string_input
 
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
print(output_string)
cv2.imshow('img', img)



cv2.waitKey(0)