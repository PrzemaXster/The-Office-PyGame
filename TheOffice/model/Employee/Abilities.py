import random


class Abilities:
    def __init__(self, stomach=-1, boredom=-1, anxiety=-1, speed=-1):
        if stomach != -1 and boredom != -1 and anxiety != -1:
            self.stomach = stomach
            self.boredom = boredom
            self.anxiety = anxiety
            self.speed = speed
        else:
            self.stomach = random.randrange(5, 10)
            self.boredom = random.randrange(3, 7)
            self.anxiety = random.randrange(4, 15)
            self.speed = random.randrange(4, 6)
        # self.inteligence = random.randrange(5, 10)
