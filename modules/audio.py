import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 9600) # Set the correct serial port and baud rate

def play_sound():
    ser.write(bytes([0x7E, 0xFF, 0x06, 0x0D, 0x00, 0x01, 0x01, 0x01, 0xFE, 0xEF])) # Send the command to play the first MP3 file on the SD card
    time.sleep(5) # Wait for 5 seconds
    ser.write(bytes([0x7E, 0xFF, 0x06, 0x0D, 0x00, 0x00, 0x01, 0x01, 0xFE, 0xEF])) # Send the command to stop playing the MP3 file

play_sound() # Call the function to play the MP3 file
