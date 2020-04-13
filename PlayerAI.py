import sys
import time
from BaseAI import BaseAI

from collections import deque
from Displayer  import Displayer

# Time Limit Before Losing
timeLimit = 0.07
maxTimeLimit = 0.15
minTimeLimit = timeLimit

class PlayerAI(BaseAI):
    def __init__(self, size = 4):
        self.__frontier = deque()
        self.__displayer = Displayer()
        self.__size = size
        self.__possibleNewTiles = [2, 4]
        self.__range = 2
        self.__free_tile_value = 20
        self.__max_free_tile_value = self.__free_tile_value + 2
        self.__bonus = 16
        self.__weigths = ([0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6])
        self.__depth = 0
        #
        # [0,1,2,3]
        # [1,2,3,4]
        # [2,3,4,5]
        # [3,4,5,6]
        #
        sys.setrecursionlimit(20000)

    def getMove(self, grid):
        self.prevTime = time.clock()
        self.__depth = 0
        (move, state, v) = self.maximize(grid, -sys.maxint, sys.maxint)
        print ("Depth: ", self.__depth)
        return move

    #state.children para max son los cuatro posibles movimientos
    #               para min son todos los cuadros vacios * 2
    def maximize(self, state, alpha, beta):
        self.__depth = self.__depth + 1
        if self.terminal_test(state):
            return None, None, self.utility(state)
        (move, maxChild, maxUtility) = (None, None, -sys.maxint)
        for mov in state.getAvailableMoves():
            child = state.clone()
            child.move(mov)
            (trash, trash, utility) = self.minimize(child, alpha, beta)
            if utility > maxUtility:
                (move, maxChild, maxUtility) = (mov, child, utility)
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return move, maxChild, maxUtility

    def minimize(self, state, alpha, beta):
        self.__depth = self.__depth + 1
        if self.terminal_test(state):
            return None, None, self.utility(state)
        (move, minChild, minUtility) = (None, None, sys.maxint)
        for x in xrange(self.__size):
            for y in xrange(self.__size):
                for i in xrange(self.__range):
                    if not state.map[x][y] == 0:
                        break
                    else:
                        child = state.clone()
                        child.map[x][y] = self.__possibleNewTiles[i]
                        (trash, trash, utility) = self.maximize(child, alpha, beta)
                        if utility < minUtility:
                            (move, minChild, minUtility) = (None, child, utility)
                        if minUtility <= alpha:
                            break
                        if minUtility < beta:
                            beta = minUtility
        return move, minChild, minUtility

    def terminal_test(self, state):
        if not state.canMove():
            return True
        return self.updateAlarm(time.clock())

    def utility(self, state):
        score = 0
        penalization = 0
        free_tiles = 0
        for x in xrange(self.__size):
            for y in xrange(self.__size):
                if state.map[x][y] == 0:
                    free_tiles += 1
                score += self.__weigths[x][y] * state.map[x][y]
                if x > 0:
                    penalization += state.map[x][y] - state.map[x-1][y]
                    if state.map[x][y] == state.map[x-1][y]:
                        score += self.__bonus + (state.map[x][y] + self.__weigths[x][y]) / 2
                if x < self.__size - 1:
                    penalization += state.map[x][y] - state.map[x+1][y]
                    if state.map[x][y] == state.map[x+1][y]:
                        score += self.__bonus + (state.map[x][y] + self.__weigths[x][y]) / 2
                if y > 0:
                    penalization += state.map[x][y] - state.map[x][y-1]
                    if state.map[x][y] == state.map[x][y-1]:
                        score += self.__bonus + (state.map[x][y] + self.__weigths[x][y]) / 2
                if y < self.__size - 1:
                    penalization += state.map[x][y] - state.map[x][y+1]
                    if state.map[x][y] == state.map[x][y+1]:
                        score += self.__bonus + (state.map[x][y] + self.__weigths[x][y]) / 2
        if free_tiles < 5:
            timeLimit = maxTimeLimit
            self.__free_tile_value = self.__max_free_tile_value
        else:
            timeLimit = minTimeLimit
        free_tiles *= self.__free_tile_value
        return score - penalization + free_tiles

    def updateAlarm(self, currTime):
        return currTime - self.prevTime > timeLimit
