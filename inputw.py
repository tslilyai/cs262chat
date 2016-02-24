import curses
import sys
import random
import time

class InputWindow:
    line = ""
    screen = None
            
    def __init__(self, window):
        self.screen = window
        self.screen.border(0)
        
    def putchar(self, c):
        line += c

    def clearLine(self):
        line = ""

    def displayScreen(self):
        # clear screen
        self.screen.erase()
        self.screen.addstr(0, 0, line)

    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()
