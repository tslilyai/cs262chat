import curses
import sys
import random
import time

class InputWindow:
    line = ""
    screen = None
            
    def __init__(self, window):
        self.screen = window
        self.screen.refresh()
        
    def putchar(self, c):
        if c == ord('\b') or c == curses.KEY_BACKSPACE or c == curses.KEY_DC or c == 127:
            with open('log.txt', 'a') as f:
                f.write('Erased %s ' %self.line)
            self.line = self.line[:-1]
        else:
            self.line += chr(c)  

    def clearLine(self):
        self.line = ""

    def displayScreen(self):
        # clear screen
        self.screen.erase()
        self.screen.addstr(2, 0, self.line)
        self.screen.refresh()
