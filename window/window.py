import curses
import sys
import random
import time
from display import DisplayScreen
from inputw import InputWindow
import os

import thread

from protocols import Message

class LoginUser(object):
    def __init__(self, username, u_id, checkpoint = 0):
        self.username = username
        self.u_id = u_id
        self.checkpoint = checkpoint
        self.messages = {}
        self.formatted_messages = {}

    def add_message(self, message):
        if to_id not in self.messages:
            self.messages[message.to_id] = []
            self.formatted_messages = {}
        self.messages[message.to_id].append(message)
        self.formatted_messages[message.to_id].append(
            '%s: %s' % (message.from_name, message.msg))

# When you enter conversation mode,
# call setLines(self.current_user.formatted_messages[self.mode])
# When you enter command mode
# call setLines(self.cmd_history)
class Application(object):
    DOWN = 1
    UP = -1
    ESC_KEY = 27

    screen = None
    cmd_history = []
    prompt = "> "
    num_args = {
            "login" : 1,
            "mk-user" : 1,
            "ls-groups" : 0,
            "ls-users" : 0,
            "ls-group-members" : 1,
            "mk-group" : 1,
            "add-group-member" : 2,
            "remove-group-member" : 2,
            "talk-with" : 2,
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
            "talk-with",
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
            "talk-with [group/user] [group or user name]*",
            "logout*",
            "*must be logged in"
    } 

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

        self.current_user = None
        self.mode = -1

    def poll_for_messages(self, delay = 1):
        try:
            while(1):
                time.sleep(delay)
                if self.current_user is None:
                    continue
                msgs = self.P.fetch_messages(self.current_user.u_id, checkpoint)
                # TODO: concurrency
                for m in msgs:
                    self.current_user.add_message(m)
                self.displayScreen()
        except KeyboardInterrupt:
            return
        
    def run(self):
        thread.start_new_thread(self.poll_for_messages, tuple())
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
                    self.mode = -1
                elif c == ord('\n'):
                    # Interpret command
                    if self.mode == -1:
                        self.display.setLines(cmd_history)
                        self.execute_cmd(self.input_w.line)
                    else:
                        self.display.setLines(self.current_user.formatted_messages)
                        self.P.send_message(from_name=current_user.username,
                                            dest_id=self.mode,
                                            msg=self.input_w.line)
                    self.input_w.clearLine()
                else:
                    self.input_w.putchar(c)
            except Exception as e:
                with open ("log.txt", "a") as f:
                    f.write("CRASHED %s\n" % e)

    def displayScreen(self):
        self.display.displayScreen()
        self.input_w.displayScreen()

    def addCmdLine(self, line):
        self.cmd_history.append(line)

    def execute_cmd(self, cmd):
        cmd_args = cmd.strip().split()[0]
        is_valid = cmd_args[0] in self.valid_cmds and self.num_args[cmd_args[0]] == len(cmd_args[1:])
        if not is_valid_cmd:
            self.addCmdLine("Invalid Command! Valid commands and usage:")
            for line in usage:
                self.addCmdLine("\t" + line)
        else:
            # add the cmd to the outputLines
            cmd_line = prompt
            for arg in cmd_args:
                cmd_line += args + " "
            self.addCmdLine(cmd_line)
            
            # execute the cmd
            if cmd_args[0] == "login":
                username = cmd_args[1]
                users = self.P.list_accounts(username)
                if users == []:
                    self.addCmdLine("Username %s does not exist. Please create a new account." % cmd_args[1])
                else: 
                    user = users[0]
                    self.current_user = LoginUser(user.username, user.u_id)
                    self.addCmdLine("Logged in as %s" % cmd_args[1])
            elif cmd_args[0] == "mk-user":
                self.P.username = cmd_args[1]
                response = self.P.create_account(cmd_args[1])
                if response is None:
                    self.addCmdLine("Created account and logged in as %s" % cmd_args[1])
                else:
                    self.addCmdLine(response)
            elif cmd_args[0] == "ls-groups":
                response = self.P.list_groups() if len(cmd_args) == 1 else self.P.list_groups(cmd_args[1])
                for group in response:
                    self.addCmdLine("Group Name: %s\t Group ID: %d" % group)
            elif cmd_args[0] == "ls-users":
                response = self.P.list_accounts() if len(cmd_args) == 1 else self.P.list_accounts(cmd_args[1])
                for user in response:
                    self.addCmdLine("Username: %s\t User ID: %d" % user)
            elif cmd_args[0] == "ls-group-members":
                response = self.P.list_group_members(cmd_args[1])
                for user in response:
                    self.addCmdLine("Username: %s\t User ID: %d" % user)
            elif cmd_args[0] == "mk-group":
                response = self.P.create_group(cmd_args[1])
                if response is None:
                    self.addCmdLine("Created group %s" % cmd_args[1])
                else:
                    self.addCmdLine(response)
            elif cmd_args[0] == "add-group-member":
                response = self.P.add_group_member(cmd_args[1], cmd_args[2])
                if response is None:
                    self.addCmdLine("Added %s from group %s" % (cmd_args[2], cmd_args[1]))
                else:
                    self.addCmdLine(response)
            elif cmd_args[0] == "remove-group-member":
                response = self.P.remove_group_member(cmd_args[1], cmd_args[2])
                if response is None:
                    self.addCmdLine("Removed %s from group %s" % (cmd_args[2], cmd_args[1]))
                else:
                    self.addCmdLine(response)
            elif cmd_args[0] == "logout":
                self.current_user = None
                self.addCmdLine("Logged out of account %s" % self.P.username)
            elif cmd_args[0] == "talk-with":
                tpe = cmd_args[1]
                if tpe != "user" or tpe != "group":
                    self.addCmdLine("Type of conversation must be either user or group.")
                to_name = cmd_args[2]
                if tpe == "user":
                    convo_id = self.P.create_conversation(self.current_user.username, cmd_args[1])
                    self.mode = convo_id
                elif tpe == "group":
                    groups = self.P.list_groups(to_name)
                    if groups == []:
                        self.addCmdLine("Group %s does not exist." % to_name)
                    else:
                        self.mode = groups[0].g_id
                return
