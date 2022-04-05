# from ode.constants import *


def hit(accuracy, evasion):
    roll = 1 - (accuracy * 1.25 / (accuracy + (evasion * 0.2)*0.9))
    return roll


print(hit(80,100))