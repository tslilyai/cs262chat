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
        with open ("log.txt", "a") as f:
            f.write("put a char%c\n" % c)
        self.line += chr(c)  

    def clearLine(self):
        with open ("log.txt", "a") as f:
            f.write("cleared a line")
        self.line = ""

    def displayScreen(self):
        # clear screen
        self.screen.erase()
        self.screen.addstr(0, 0, self.line)
