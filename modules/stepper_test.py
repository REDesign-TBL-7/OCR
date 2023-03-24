import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit2 = MotorKit(address=0x60)
kit3 = MotorKit(address=0x61)

def stepper_test():
    for i in range(7):
        for j in range(291):
            kit3.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            kit2.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        time.sleep(1)

if __name__ == "__main__":
    stepper_test()
