import curses
import sys
import random
import time
from display import DisplayScreen
from inputw import InputWindow
import os

class Window:
    DOWN = 1
    UP = -1
    ESC_KEY = 27

    screen = None
            
    def __init__(self, screen):
        self.screen = screen
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1) 
        self.screen.border(0)

        height, width = self.screen.getmaxyx()
        display_window = curses.newwin(height - 10, width, 1, 1)
        input_window = curses.newwin(5, width, height-10, 1)
        self.display = DisplayScreen(display_window)
        self.input_w = InputWindow(input_window)
        self.run()
        
    def run(self):
        while True:
            assert not curses.isendwin()
            try:
                self.displayScreen()
                # get user command
                c = self.screen.getch()
                with open ("log.txt", "a") as f:
                    f.write("Read %d\n" % c)
                if c == curses.KEY_UP: 
                    self.display.updown(self.UP)
                elif c == curses.KEY_DOWN:
                    self.display.updown(self.DOWN)
                elif c == self.ESC_KEY:
                    sys.exit()
                elif c == ord('\n'):
                    self.flush_screen()
                else:
                    self.input_w.putchar(c)
            except Exception as e:
                with open ("log.txt", "a") as f:
                    f.write("CRASHED %s\n" % e)

    def flush_screen(self):
        self.display.addOutputLine(self.input_w.line)
        self.input_w.clearLine()

    def displayScreen(self):
        self.display.displayScreen()
        self.input_w.displayScreen()

def main(screen):
    ih = Window(screen)

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
