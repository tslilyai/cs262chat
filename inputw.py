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
        self.line += chr(c)  

    def clearLine(self):
        self.line = ""

    def displayScreen(self):
        # clear screen
        self.screen.erase()
        self.screen.addstr(2, 0, self.line)
        self.screen.refresh()
