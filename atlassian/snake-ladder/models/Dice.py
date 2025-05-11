

from random import randint


class Dice:
    def __init__(self, min_val = 1, max_val = 6) -> None:
        self.max = max
        self.min = min
    
    def roll(self):
        return randint(self.min, self.max)