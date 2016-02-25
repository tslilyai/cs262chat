import curses
import sys
import random
import time
from display import DisplayScreen
from inputw import InputWindow

class Window:
    DOWN = 1
    UP = -1
    ESC_KEY = 27

    screen = None
            
    def __init__(self):
        self.screen = curses.initscr()
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
            try:
                self.displayScreen()
                # get user command
                c = self.screen.getch()
                if c == curses.KEY_UP: 
                    self.display.updown(self.UP)
                elif c == curses.KEY_DOWN:
                    self.display.updown(self.DOWN)
                elif c == self.ESC_KEY:
                    self.exit()
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
'''
    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()
'''
def main(arg):
    ih = Window()

if __name__ == "__main__":
    curses.wrapper(main)
