import curses

class InputWindow(object):
    line = ""
    pos = 0
    screen = None
            
    def __init__(self, window):
        self.screen = window
        self.screen.refresh()
        self.history = []
        self.historypos = 0
        
    def putchar(self, c):
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
        self.history.append(self.line)
        self.historypos = 0
        self.line = ""
        self.pos = 0

    def displayScreen(self):
        self.screen.erase()
        self.screen.hline(0, 0, '-', self.screen.getmaxyx()[1])
        self.screen.addstr(1, 0, self.line)
        self.screen.move(1, self.pos)
        self.screen.refresh()
