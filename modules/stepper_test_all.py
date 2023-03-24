import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)
kit3 = MotorKit(address=0x62)
kit4 = MotorKit(address=0x63)

def stepper_test():
    for i in range(7):
        for j in range(291):
            kit1.stepper1.onestep()
            kit1.stepper2.onestep()
            kit2.stepper1.onestep()
            kit3.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            kit2.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            kit3.stepper2.onestep()
            kit4.stepper1.onestep()
            kit4.stepper2.onestep()
        time.sleep(1)

if __name__ == "__main__":
    stepper_test()
