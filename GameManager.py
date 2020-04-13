from Grid       import Grid
from ComputerAI import ComputerAI
from PlayerAI   import PlayerAI
from Displayer  import Displayer
from random     import randint
import time

_DEBUG_LEVEL = 0

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05


class GameManager:
    def __init__(self, size=4):
        self.__grid = Grid(size)
        self.__possibleNewTiles = [2, 4]
        self.__probability = defaultProbability
        self.__initTiles = defaultInitialTiles
        self.__computerAI = None
        self.__playerAI = None
        self.__displayer = None
        self.__over = False
        self.__prevTime = None

    def setComputerAI(self, computerAI):
        self.__computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.__playerAI = playerAI

    def setDisplayer(self, displayer):
        self.__displayer = displayer

    def updateAlarm(self, currTime):
        if currTime - self.__prevTime > timeLimit + allowance:
            self.__over = True
        else:
            while time.clock() - self.__prevTime < timeLimit + allowance:
                pass

            self.__prevTime = time.clock()

    def updateAlarmTrick(self, currTime):
        self.__over = False

    def start(self):
        for i in xrange(self.__initTiles):
            self.insertRandonTile()

        self.__displayer.display(self.__grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.__prevTime = time.clock()

        while not self.isGameOver() and not self.__over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.__grid.clone()

            move = None

            if turn == PLAYER_TURN:
                print "Player's Turn:",
                move = self.__playerAI.getMove(gridCopy)
                print actionDic[move]

                # Validate Move
                if move is not None and 0 <= move < 4:
                    if self.__grid.canMove([move]):
                        self.__grid.move(move)

                        # Update maxTile
                        maxTile = self.__grid.getMaxTile()
                    else:
                        print "Invalid PlayerAI Move"
                        self.__over = True
                else:
                    print "Invalid PlayerAI Move - 1"
                    self.__over = True
            else:
                print "Computer's turn:"
                move = self.__computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.__grid.canInsert(move):
                    self.__grid.setCellValue(move, self.getNewTileValue())
                else:
                    print "Invalid Computer AI Move"
                    self.__over = True

            if not self.__over:
                self.__displayer.display(self.__grid)

            # Exceeding the Time Allotted for Any Turn Terminates the Game
            if _DEBUG_LEVEL == 0:
                self.updateAlarm(time.clock())
            else:
                self.updateAlarmTrick(time.clock())

            turn = 1 - turn
        print maxTile
        #print self.__playerAI.getMaxDepth()

    def isGameOver(self):
        return not self.__grid.canMove()

    def getNewTileValue(self):
        if randint(0,99) < 100 * self.__probability:
            return self.__possibleNewTiles[0]
        else:
            return self.__possibleNewTiles[1]

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.__grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.__grid.setCellValue(cell, tileValue)


def main():
    gameManager = GameManager()
    playerAI = PlayerAI()
    computerAI = ComputerAI()
    displayer = Displayer()

    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)

    gameManager.start()


if __name__ == '__main__':
    main()
