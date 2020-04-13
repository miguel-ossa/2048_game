from BaseDisplayer import BaseDisplayer
from Grid import Grid
import platform
from graphics import *
from copy import deepcopy
import os

_DEBUG_LEVEL = 0

colorMap = {
    0: 97,
    2: 40,
    4: 100,
    8: 47,
    16: 107,
    32: 46,
    64: 106,
    128: 44,
    256: 104,
    512: 42,
    1024: 102,
    2048: 43,
    4096: 103,
    8192: 45,
    16384: 105,
    32768: 41,
    65536: 101,
}

cTemp = "\x1b[%dm%7s\x1b[0m "


class Displayer(BaseDisplayer):
    def __init__(self, size=4):
        self.__size = size
        self.__screen_size = self.__size * 100
        self.__square_size = self.__screen_size / self.__size
        self.__win = None
        self.__my_grid = None
        if "Windows" == platform.system():
            self.display = self.winDisplay
        else:
            self.display = self.unixDisplay

    def display(self, grid):
        pass

    def openVGrid(self):
        self.__win = GraphWin("2048", self.__screen_size, self.__screen_size)
        self.__win.setBackground("black")
        for y in range(self.__size):
            for x in range(self.__size):
                rect = Rectangle(Point(self.__square_size * x, self.__square_size * y),
                                 Point(self.__square_size * (x + 1), self.__square_size * (y + 1)))
                rect.setOutline("white")
                rect.setWidth(5)
                rect.draw(self.__win)
        return

    def printVGrid(self, grid):
        if self.__my_grid is not None:
            i = 0
            for y in range(self.__size):
                for x in range(self.__size):
                    message = Text(Point(self.__square_size * x + self.__square_size / 2,
                                         self.__square_size * y + self.__square_size / 2), self.__my_grid.map[x][y])
                    message.setSize(35)
                    message.setTextColor("black")
                    message.draw(self.__win)
                    i = i + 1
        i = 0
        for y in range(self.__size):
            for x in range(self.__size):
                message = Text(Point(self.__square_size * x + self.__square_size / 2,
                                     self.__square_size * y + self.__square_size / 2), grid.map[x][y])
                message.setSize(35)
                if grid.map[x][y] == 0:
                    message.setTextColor("green")
                else:
                    message.setTextColor("gray")
                message.draw(self.__win)
                i = i + 1

        self.__my_grid = Grid()
        self.__my_grid.map = deepcopy(grid.map)
        self.__my_grid.size = grid.getSize()

        #time.sleep(0.3)
        return


    def closeVGrid(self):
        self.__win.close()


    def winDisplay(self, grid):
        for i in xrange(grid.getSize()):
            for j in xrange(grid.getSize()):
                print "%6d  " % grid.map[i][j],
            print ""
        print ""

    def unixDisplay(self, grid):
        if _DEBUG_LEVEL > 0:
            print ""
        for i in xrange(3 * grid.getSize()):
            for j in xrange(grid.getSize()):
                v = grid.map[i / 3][j]

                if i % 3 == 1:
                    if _DEBUG_LEVEL > 0:
                        string = str(v).center(3, " ")
                    else:
                        string = str(v).center(7, " ")
                else:
                    string = " "

                if _DEBUG_LEVEL > 0:
                    if i % 3 == 1:
                        print string,
                else:
                    print cTemp %  (colorMap[v], string),
            if _DEBUG_LEVEL == 0:
                print ""

            if i % 3 == 2:
                print ""
