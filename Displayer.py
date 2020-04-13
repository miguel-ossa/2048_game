from BaseDisplayer import BaseDisplayer
import platform
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
    def __init__(self):
        if "Windows" == platform.system():
            self.display = self.winDisplay
        else:
            self.display = self.unixDisplay

    def display(self, grid):
        pass

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
