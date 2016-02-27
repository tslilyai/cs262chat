"""
Lyle Scott, III
lyle@digitalfoo.net
A simple demo that uses curses to scroll the terminal.
"""

import curses
import sys
import random
import time
import thread

class DisplayScreen:
    DOWN = 1
    UP = -1
    ESC_KEY = 27

    outputLines = []
    screen = None
            
    def __init__(self, window):
        self.screen = window
        self.screen.border(0)
        self.topLineNum = 0
        self.markedLineNums = []
        self.getOutputLines()        


    def setLines(self, lines, adjust=False):
        was_last_page = self.topLineNum + self.screen.getmaxyx()[0] >= self.nOutputLines + 1
        self.outputLines = lines
        self.nOutputLines = len(lines)
        if adjust:
            self.topLineNum = max(0, self.nOutputLines - self.screen.getmaxyx()[0] + 1)
        else:
            if was_last_page:
                self.topLineNum = max(0, self.nOutputLines - self.screen.getmaxyx()[0] + 1)

        self.displayScreen()

    def getOutputLines(self):
        self.nOutputLines = len(self.outputLines)

    def addOutputLine(self, line):
        self.outputLines.append(line)
        self.nOutputLines += 1
        if self.topLineNum + self.screen.getmaxyx()[0] == self.nOutputLines:
            self.topLineNum+=1
        self.displayScreen()

    def displayScreen(self):
        # clear screen
        self.screen.erase()

        # now paint the rows
        top = self.topLineNum
        bottom = self.topLineNum+self.screen.getmaxyx()[0]
        for (index,line,) in enumerate(self.outputLines[top:bottom]):
            linenum = self.topLineNum + index
            self.screen.addstr(index, 0, line)
        self.screen.refresh()

    def updown(self, increment):
        with open('log.txt', 'a') as f:
            f.write('top: %d\n'% self.topLineNum)
        if increment == self.UP and self.topLineNum > 0:
            self.topLineNum += self.UP 
            return
        elif increment == self.DOWN and (self.topLineNum+self.screen.getmaxyx()[0]-1) < self.nOutputLines:
            self.topLineNum += self.DOWN
            return
