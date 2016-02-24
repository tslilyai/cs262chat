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
    SPACE_KEY = 32
    ESC_KEY = 27

    outputLines = []
    screen = None
            
    def __init__(self, window):
        self.screen = window
        self.screen.border(0)
        self.topLineNum = 0
        self.highlightLineNum = 0
        self.markedLineNums = []
        self.getOutputLines()        

 
        # thread that just adds lines
        def add_lines(v):
            while(1):
                try:
                    self.addOutputLine("this is a line")
                except KeyboardInterrupt:
                    exit(0)
                except Exception as e:
                    with open ("log.txt", "a") as f:
                        f.write("CRASHED %s\n" % e)
                with open ("log.txt", "a") as f:
                    f.write("added a line!\n")
                time.sleep(.1)
        thread.start_new_thread(add_lines, ("this is a line\n",))

        
    def getOutputLines(self):
        self.nOutputLines = len(self.outputLines)

    def addOutputLine(self, line):
        self.outputLines.append(line)
        self.nOutputLines+=1
        self.displayScreen()

    def displayScreen(self):
        # clear screen
        self.screen.erase()

        # now paint the rows
        top = self.topLineNum
        bottom = self.topLineNum+self.screen.getmaxyx()[0]
        for (index,line,) in enumerate(self.outputLines[top:bottom]):
            linenum = self.topLineNum + index

            # highlight current line            
            if index != self.highlightLineNum:
                self.screen.addstr(index, 0, line)
            else:
                self.screen.addstr(index, 0, line, curses.A_BOLD)
        self.screen.refresh()

    # move highlight up/down one line
    def updown(self, increment):
        nextLineNum = self.highlightLineNum + increment
        with open ("log.txt", "a") as f:
            f.write("running updown")

        # paging
        if increment == self.UP and self.highlightLineNum == 0 and self.topLineNum != 0:
            self.topLineNum += self.UP 
            return
        elif increment == self.DOWN and nextLineNum == curses.LINES and (self.topLineNum+curses.LINES) != self.nOutputLines:
            self.topLineNum += self.DOWN
            return

        # scroll highlight line
        if increment == self.UP and (self.topLineNum != 0 or self.highlightLineNum != 0):
            self.highlightLineNum = nextLineNum
        elif increment == self.DOWN and (self.topLineNum+self.highlightLineNum+1) != self.nOutputLines and self.highlightLineNum != curses.LINES:
            self.highlightLineNum = nextLineNum
 
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()