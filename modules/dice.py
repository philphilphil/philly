import random

def dice(phenny, input):
    return phenny.say(str(random.randint(1,6)))

dice.commands = ['dice']
