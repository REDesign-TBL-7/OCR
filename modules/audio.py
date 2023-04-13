import serial

# Open a serial connection to the DFPlayer Mini
ser = serial.Serial('/dev/ttyS0', 9600)

# Send a command to the DFPlayer Mini
def send_cmd(cmd, feedback=True):
    # Create a bytearray with the command and checksum
    data = bytearray([0x7e, 0xff, 0x06, cmd >> 8, cmd & 0xff, 0x00, 0x00, 0x00, 0xef])

    # Send the command to the DFPlayer Mini
    ser.write(data)

    # Wait for feedback if enabled
    if feedback:
        while True:
            if ser.read() == b'\x7e':
                if ser.read() == b'\xff':
                    if ser.read() == b'\x06':
                        if ser.read() == b'\x00':
                            if ser.read() == b'\x00':
                                if ser.read() == b'\x00':
                                    if ser.read() == b'\xfe':
                                        if ser.read() == b'\xef':
                                            break

# Set the volume to 50%
send_cmd(0x0605, feedback=False)
send_cmd(0x0601, feedback=False)
send_cmd(0x0600, feedback=False)

# Play track 001
send_cmd(0x0301)
