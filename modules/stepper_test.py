import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--backward", action="store_true", help="direction of the motors")
parser.add_argument("-s", "--steps", type=int, help="number of steps to turn (One revolution = 2037)")
parser.add_argument("-id", "--id", nargs="*", type=int, help="IDs of Motors to turn")
parser.add_argument("-d", "--double", action="store_true", help="stepper motor Mode")

args = parser.parse_args()

motor_list = [x for x in args.id if x >= 0 and x <=7]
motor_set = set(args.id)

style = stepper.DOUBLE if args.double else stepper.SINGLE
direction = stepper.BACKWARD if args.backward else stepper.FORWARD

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)
kit3 = MotorKit(address=0x62)
kit4 = MotorKit(address=0x63)

def stepper_test():
    for i in range(770 if args.steps == None else args.steps):
        if 0 in motor_set:
            kit1.stepper1.onestep(direction=direction, style=style)
        if 1 in motor_set:
            kit1.stepper2.onestep(direction=direction, style=style)
        if 2 in motor_set:
            kit2.stepper1.onestep(direction=direction, style=style)
        if 3 in motor_set:
            kit2.stepper2.onestep(direction=direction, style=style)
        if 4 in motor_set:
            kit3.stepper1.onestep(direction=direction, style=style)
        if 5 in motor_set:
            kit3.stepper2.onestep(direction=direction, style=style)
        if 6 in motor_set:
            kit4.stepper1.onestep(direction=direction, style=style)
        if 7 in motor_set:
            kit4.stepper2.onestep(direction=direction, style=style)

if __name__ == "__main__":
    stepper_test()
