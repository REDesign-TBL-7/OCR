numBraille = 6

testing = ['000001', '110010', '100010', '111000', '111000', '100000', '000000']

cache = ['000000'] * numBraille

def raiseGear(cache, cur):
    # to be filled
    return
def lowerGear():
    # to be filled
    return
def waitforbuttonpress():
    # to be filled
    return

for cur in range(numBraille):
    for i in range(6):
        if (testing[cur][i]==cache[cur][i]):
            lowerGear()
        else:
            raiseGear()
        spinGear()
    waitforbuttonpress()


