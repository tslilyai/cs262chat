import curses
import sys
import random
import time

class InputWindow(object):
    line = ""
    pos = 0
    screen = None
            
    def __init__(self, window):
        self.screen = window
        self.screen.refresh()
        
    def putchar(self, c):
        if c == ord('\b') or c == curses.KEY_BACKSPACE or c == curses.KEY_DC or c == 127:
            self.line = self.line[:-1]
            self.pos -= 1
        elif c == curses.KEY_LEFT:
            if self.pos > 0:
                self.pos -= 1
        elif c == curses.KEY_RIGHT:
            if self.pos < len(self.line):
                self.pos += 1
        elif curses.keyname(c) == '^A':
            self.pos = 0
        elif curses.keyname(c) == '^E':
            self.pos = len(self.line)
        elif curses.keyname(c) == '^U':
            self.line = self.line[self.pos:]
            self.pos = 0
        elif curses.keyname(c) == '^K':
            self.line = self.line[:self.pos]
        else:
            self.line = self.line[:self.pos] + chr(c) + self.line[self.pos:]
            self.pos += 1

    def clearLine(self):
        self.line = ""
        self.pos = 0

    def displayScreen(self):
        self.screen.erase()
        self.screen.hline(0, 0, '-', self.screen.getmaxyx()[1])
        self.screen.addstr(1, 0, self.line)
        self.screen.move(1, self.pos)
        self.screen.refresh()
