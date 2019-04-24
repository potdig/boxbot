import random
import numpy


class LotteryBox():
    def __init__(self, contents):
        self._contents = contents
        random.shuffle(self._contents)

    def pick(self):
        return self._contents.pop()

    def remove(self, cont):
        self._contents.remove(cont)

    def team(self, team_count):
        return numpy.array_split(self._contents, team_count)

    def size(self):
        return len(self._contents)
