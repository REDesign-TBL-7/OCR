import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(address=0x64)

def stepper_test():
    for i in range(7):
        for j in range(291):
            kit.stepper1.onestep()
            kit.stepper2.onestep()
        time.sleep(1)

if __name__ == "__main__":
    stepper_test()
