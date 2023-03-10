import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(address=0x63)
direction = "B"
STEPS = 340
def stepper_test():
    for j in range(STEPS):
        kit.stepper1.onestep()
        # kit.stepper2.onestep()
    time.sleep(1)

if __name__ == "__main__":
    stepper_test()
