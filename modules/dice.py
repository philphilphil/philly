import random

def dice(phenny, input):
    random.seed()

    if not input.group(2):
        return phenny.say(str(random.randint(1,6)))

    count = 1
    c = []
    while count <= int(input.group(2)):
        rand = str(random.randint(1,6))
        c.append(rand)
        count += 1

    return phenny.say(' '.join(c))
dice.commands = ['dice']
