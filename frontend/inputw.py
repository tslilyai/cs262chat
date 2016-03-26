import curses

class InputWindow(object):
    '''
    InputWindow defines a curses screen in which a user can
    type input commands, and have this input displayed on the screen and 
    interpreted by the running application.
    '''

    line = ""
    pos = 0
    screen = None
            
    def __init__(self, window):
        '''
        Initialize an input window, setting the history of commands to empty and
        refreshing the screen so that the window appears blank. This is initialized 
        during creation of an Application object.

        :param window: the curses window object which should represent the input screen
        :return: InputWindow object
        '''
        self.screen = window
        self.screen.refresh()
        self.history = []
        self.historypos = 0
        
    def putchar(self, c):
        '''
        Writes a character to the input window. The written characters are also logged
        to a log file (log.txt).
        Special keys, such as arrow keys, shift the position of the cursor on the window
        screen or display a history of commands.
        Deletion of characters is also supported.

        :param c: the character to display on the screen 
        :return: void
        '''
        with open('log.txt', 'a') as f:
            f.write('Received %s\n' % curses.keyname(c))
        if c == ord('\b') or c == curses.KEY_BACKSPACE or c == curses.KEY_DC or c == 127:
            self.line = self.line[:-1]
            if self.pos > 0:
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
        elif c == curses.KEY_SR:
            if self.historypos > -len(self.history):
                self.historypos -= 1
                self.line = self.history[self.historypos]
                self.pos = len(self.line)
        elif c == curses.KEY_SF:
            if self.historypos < -1:
                self.historypos += 1
                self.line = self.history[self.historypos]
                self.pos = len(self.line)
        else:
            self.line = self.line[:self.pos] + chr(c) + self.line[self.pos:]
            self.pos += 1

    def clearLine(self):
        '''
        Clear the current command line, and add this to the command history
        in case the user wishes to retrieve their previous commands.

        :return: void
        '''
        self.history.append(self.line)
        self.historypos = 0
        self.line = ""
        self.pos = 0

    def displayScreen(self):
        '''
        Refreshes the input window screen and displays the current value
        of the command line.
        This is called by the application to continuously show the user the
        current value of the input window after the user types a character.

        :return: void
        '''
        self.screen.erase()
        self.screen.hline(0, 0, '-', self.screen.getmaxyx()[1])
        self.screen.addstr(1, 0, self.line)
        self.screen.move(1, self.pos)
        self.screen.refresh()
