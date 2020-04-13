from random import randint
from BaseAI import BaseAI


class ComputerAI(BaseAI):
    def __init__(self):
        pass

    def getMove(self, grid):
        cells = grid.getAvailableCells()

        return cells[randint(0, len(cells) - 1)] if cells else None
