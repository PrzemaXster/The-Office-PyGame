import random


class Interests:
    def __init__(self, jokes=-1, technology=-1, sports=-1):
        self.MAX_INTEREST = 5
        if jokes != -1 and technology != -1 and sports != -1:
            self.jokes = jokes
            self.technology = technology
            self.sports = sports
        else:
            self.disagree = 0
            self.jokes = random.randrange(1, self.MAX_INTEREST)
            self.technology = random.randrange(1, self.MAX_INTEREST)
            self.sports = random.randrange(1, self.MAX_INTEREST)
        self.interests_list = [self.disagree, self.jokes, self.technology, self.sports]

    class InterestIndex:
        DISAGREE = 0
        JOKES = 1
        TECHNOLOGY = 2
        SPORTS = 3

