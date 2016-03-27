"""
Adapted from source code provided by Lyle Scott
Original code can be obtained here:
    https://github.com/LyleScott/Python-curses-Scrolling-Example

Lyle Scott, III
lyle@digitalfoo.net
A simple demo that uses curses to scroll the terminal.
"""

import curses
import sys

class DisplayScreen:
    '''
    DisplayScreen defines a curses screen in text can be displayed.
    It also provides scrolling functionality with the arrow keys.
    '''
    DOWN = 1
    UP = -1
    ESC_KEY = 27

    outputLines = []
    screen = None
            
    def __init__(self, window):
        '''
        Initialize a display screen, setting the top line to 0 and the lines to display
        to the screen as empty.

        :param window: the curses window object which should represent the display screen
        :return: DisplayScreen object
        '''

        self.screen = window
        self.screen.border(0)
        self.topLineNum = 0
        self.markedLineNums = []
        self.nOutputLines = 0

    def setLines(self, lines, adjust=False):
        '''
        Changes the set of lines that is displayed on the display screen.
        Calculates the range of lines to display according to the following rule:
            if adjust is true, we always display the last n lines
            if adjust is not true, we display the last n lines if the previous display
                showed the last n lines; otherwise, we show the same set of lines as the previous display

        The rationale for this logic is, if the user is viewing previous messages, we don't want
        to scroll to the bottom every time a new message comes in.
        However, if we are at the very bottom, we want to see new messages, instead of having to scroll down
        to see them.

        :param lines: the lines to display on the screen
        :param adjust: if True, shows the first n lines of the set of the lines to display instead of the last n lines (default False) 
        :return: void
        '''
        was_last_page = self.topLineNum + self.screen.getmaxyx()[0] >= self.nOutputLines + 1
        self.outputLines = lines
        self.nOutputLines = len(lines)
        if adjust:
            self.topLineNum = max(0, self.nOutputLines - self.screen.getmaxyx()[0] + 1)
        else:
            if was_last_page:
                self.topLineNum = max(0, self.nOutputLines - self.screen.getmaxyx()[0] + 1)

        self.displayScreen()

    def displayScreen(self):
        '''
        Displays a page of lines on the screen. Use setLines to determine which page of lines to display.
        Called by Application object to display application output.

        :return: void
        '''
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
        '''
        Moves the set of lines to display either up or down depending on the
        user's keypress.

        :param increment: UP if the up arrow was pressed, and DOWN if the down arrow was pressed. 
                          specifies the direction in which the top line number should be moved.
        :return: void
        '''
        if increment == self.UP and self.topLineNum > 0:
            self.topLineNum += self.UP 
            return
        elif increment == self.DOWN and (self.topLineNum+self.screen.getmaxyx()[0]-1) < self.nOutputLines:
            self.topLineNum += self.DOWN
            return

    def pageup(self):
        '''
        Moves the set of lines to display up a page 

        :return: void
        '''
        self.topLineNum = max(0, self.topLineNum - (self.screen.getmaxyx()[0]-1))

    def pagedown(self):
        '''
        Moves the set of lines to display down a page 

        :return: void
        '''
        self.topLineNum = min(max(0, self.nOutputLines - self.screen.getmaxyx()[0] + 1),
                self.topLineNum + (self.screen.getmaxyx()[0]-1))
