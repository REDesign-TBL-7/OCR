import serial
import os

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

def play_sound(sound_number):
    ser.write(bytearray([0x7E, 0xFF, 0x06, 0x03, 0x00, sound_number, 0x00, 0x00, 0xEF]))

play_sound(1) # play the first sound on the DFPlayer Mini
