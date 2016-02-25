import curses
import sys
import random
import time
from display import DisplayScreen
from inputw import InputWindow
import os

class Window(object):
    DOWN = 1
    UP = -1
    ESC_KEY = 27

    screen = None
            
    def __init__(self, screen, protocol):
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
        self.P = protocol
        
    def run(self):
        pass

    def flush_screen(self):
        self.display.addOutputLine(self.input_w.line)
        self.input_w.clearLine()

    def displayScreen(self):
        self.display.displayScreen()
        self.input_w.displayScreen()

class CmdWindow(Window):
    num_args = {
            "login" : 1,
            "mk-user" : 1,
            "ls-groups" : 0,
            "ls-users" : 0,
            "ls-group-members" : 1,
            "mk-group" : 1,
            "add-group-member" : 2,
            "remove-group-member" : 2,
            "enter-conversation" : 1,
            "logout" : 0
    }
    valid_cmds = {
            "login",
            "mk-user",
            "ls-groups",
            "ls-users",
            "ls-group-members",
            "mk-user",
            "add-group-member",
            "remove-group-member",
            "enter-conversation",
            "logout"
    }
    usage = {
            "login [username]",
            "mk-user [username]",
            "ls-groups [pattern (optional)]*",
            "ls-users [pattern (optional)]*",
            "ls-group-members [groupname]*",
            "mk-group [groupname]*",
            "add-group-member [groupname] [username]*",
            "remove-group-member [groupname] [username]*",
            "enter-conversation [group or user id (use ls-groups or ls-users to get id)]*",
            "logout*",
            "*must be logged in"
    }
    
    def execute_cmd(self, cmd):
        cmd_args = cmd.strip().split()[0]
        is_valid = cmd_args[0] in self.valid_cmds and self.num_args[cmd_args[0]] == len(cmd_args[1:])
        if not is_valid_cmd:
            self.display.addOutputLine("Invalid Command! Valid commands and usage:")
            for line in usage:
                self.display.addOutputLine("\t" + line)
        else:
            if cmd_args[0] == "login":
                self.P.username = cmd_args[1]
                self.display.addOutputLine("Logged in as %s" % cmd_args[1])
            elif cmd_args[0] == "mk-user":
                self.P.username = cmd_args[1]
                response = self.P.create_account(cmd_args[1])
                if response[0]:
                    self.display.addOutputLine("Created account and logged in as %s" % cmd_args[1])
                else:
                    self.display.addOutputLine(response[1])
            elif cmd_args[0] == "ls-groups":
                response = self.P.list_groups() if len(cmd_args) == 1 else self.P.list_groups(cmd_args[1])
                for group in response:
                    self.display.addOutputLine("Group Name: %s\t Group ID: %d" % group)
            elif cmd_args[0] == "ls-users":
                response = self.P.list_accounts() if len(cmd_args) == 1 else self.P.list_accounts(cmd_args[1])
                for user in response:
                    self.display.addOutputLine("Username: %s\t User ID: %d" % user)
            elif cmd_args[0] == "ls-group-members":
                response = self.P.list_group_members(cmd_args[1])
                for user in response:
                    self.display.addOutputLine("Username: %s\t User ID: %d" % user)
            elif cmd_args[0] == "mk-group":
                response = self.P.create_group(cmd_args[1])
                if response[0]:
                    self.display.addOutputLine("Created group %s" % cmd_args[1])
                else:
                    self.display.addOutputLine(response[1])
            elif cmd_args[0] == "add-group-member":
                response = self.P.add_group_member(cmd_args[1], cmd_args[2])
                if response[0]:
                    self.display.addOutputLine("Added %s from group %s" % (cmd_args[2], cmd_args[1]))
                else:
                    self.display.addOutputLine(response[1])
            elif cmd_args[0] == "remove-group-member":
                response = self.P.remove_group_member(cmd_args[1], cmd_args[2])
                if response[0]:
                    self.display.addOutputLine("Removed %s from group %s" % (cmd_args[2], cmd_args[1]))
                else:
                    self.display.addOutputLine(response[1])
            elif cmd_args[0] == "logout":
                self.display.addOutputLine("Logged out of account %s" % self.P.username)
                self.P.username = ""
            elif cmd_args[0] == "enter-conversation":
                return cmd_args[1]                   
            return "" 

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
                    ret = self.execute_cmd()
                    if ret != "":
                        return ret
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
