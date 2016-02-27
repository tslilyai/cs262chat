import curses
import thread
import time

from frontend.display import DisplayScreen
from frontend.inputw import InputWindow
from protocols import Message

class LoginUser(object):
    def __init__(self, username, u_id, checkpoint = 0):
        self.username = username
        self.u_id = u_id
        self.checkpoint = checkpoint
        self.messages = {}
        self.formatted_messages = {}

    def add_message(self, message):
        if message.to_id not in self.messages:
            self.messages[message.to_id] = []
            self.formatted_messages[message.to_id] = []
        self.messages[message.to_id].append(message)
        self.formatted_messages[message.to_id].append(
            '%s: %s' % (message.from_name, message.msg))
        self.checkpoint = message.m_id

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
            "help" : {0, 1},
            "login" : {1},
            "mk-user" : {1},
            "ls-groups" : {0, 1},
            "ls-users" : {0, 1},
            "ls-group-members" : {1},
            "mk-group" : {1},
            "add-group-member" : {2},
            "remove-group-member" : {2},
            "talk-with" : {2},
            "logout" : {0},
    }
    usage = {
            'login': "login [username]",
            'mk_user': "mk-user [username]",
            'ls-groups': "ls-groups [pattern (optional)]*",
            'ls-users': "ls-users [pattern (optional)]*",
            'ls-group-members': "ls-group-members [g_name]*",
            'mk-group': "mk-group [g_name]*",
            'add-group-member': "add-group-member [g_name] [username]*",
            'remove-group-member': "remove-group-member [g_name] [username]*",
            'talk-with': "talk-with [group/user] [group or user name]*",
            'logout': "logout*",
            '': "*must be logged in"
    } 

    def __init__(self, screen, protocol):
        self.screen = screen
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1) 

        self.screen.border(0)
        height, width = self.screen.getmaxyx()
        display_window = curses.newwin(height - 10, width, 1, 1)
        display_window.box()
        input_window = curses.newwin(9, width, height-10, 1)
        input_window.box()
        self.display = DisplayScreen(display_window)
        self.input_w = InputWindow(input_window)
        input_window.move(0, 0)
        self.P = protocol

        self.current_user = None
        self.mode = -1
        self.exited = False
        self.screen.refresh()
        display_window.refresh()
        input_window.refresh()

    def poll_for_messages(self, delay = 1):
        while not self.exited:
            time.sleep(delay)
            if self.current_user is None:
                continue
            msgs = self.P.fetch_messages(self.current_user.u_id, self.current_user.checkpoint)
            # TODO: concurrency
            for m in msgs:
                self.current_user.add_message(m)
            if self.mode != -1:
                # This setLines is necessary since in Python, an empty list and a nonempty list will point to different objects in memory
                self.display.setLines(self.current_user.formatted_messages[self.mode])
                self.displayScreen()
        
    def run(self):
        thread.start_new_thread(self.poll_for_messages, tuple())
        self.addCmdLine("Welcome to Chat!")
        self.addCmdLine("Login to start chatting, or type help to get a list of valid commands.")
        while True:
            try:
                assert not curses.isendwin()
                if self.mode == -1:
                    self.display.setLines(self.cmd_history)
                else:
                    if self.mode not in self.current_user.formatted_messages:
                        self.current_user.formatted_messages[self.mode] = []
                    self.display.setLines(self.current_user.formatted_messages[self.mode])
                self.displayScreen()
                # get user command
                c = self.screen.getch()
                if c == curses.KEY_UP: 
                    self.display.updown(self.UP)
                elif c == curses.KEY_DOWN:
                    self.display.updown(self.DOWN)
                elif c == self.ESC_KEY:
                    self.mode = -1
                    self.display.setLines(self.cmd_history, adjust=True)
                elif curses.keyname(c) == '^U':
                    self.display.pageup()
                elif curses.keyname(c) == '^D':
                    self.display.pagedown()
                elif c == ord('\n'):
                    # Interpret command
                    if self.mode == -1:
                        self.execute_cmd(self.input_w.line)
                    else:
                        self.P.send_message(from_name=self.current_user.username,
                                            dest_id=self.mode,
                                            msg=self.input_w.line)
                    self.input_w.clearLine()
                else:
                    self.input_w.putchar(c)
            except KeyboardInterrupt as e:
                self.exited = True
                raise e

    def displayScreen(self):
        self.display.displayScreen()
        self.input_w.displayScreen()

    def addCmdLine(self, line):
        self.cmd_history.append(line)

    def execute_cmd(self, cmd):
        # add the cmd to the outputLines
        cmd_args = cmd.strip().split()
        if not cmd_args:
            return
        self.addCmdLine(self.prompt + cmd)
        is_valid = cmd_args[0] in self.num_args and len(cmd_args[1:]) in self.num_args[cmd_args[0]] 
        if not is_valid:
            self.addCmdLine("Invalid Command! Valid commands and usage:")
            for line in self.usage.values():
                self.addCmdLine("\t" + line)
        else:
            
            # execute the cmd
            if cmd_args[0] == "help":
                if len(cmd_args) == 1:
                    self.addCmdLine("Valid commands and usage:")
                    for line in self.usage.values():
                        self.addCmdLine("\t" + line)
                    self.addCmdLine('Shortcuts:')
                    self.addCmdLine('\tCTRL-a: move cursor to start of line')
                    self.addCmdLine('\tCTRL-e: move cursor to end of line')
                    self.addCmdLine('\tCTRL-k: delete everything after cursor')
                    self.addCmdLine('\tCTRL-u: page up')
                    self.addCmdLine('\tCTRL-d: page down')
                    self.addCmdLine('\tSHIFT-UP: previous command')
                    self.addCmdLine('\tSHIFT-DOWN: next command')
                else:
                    if cmd_args[0] in self.usage:
                        self.addCmdLine(self.usage[cmd_args[1]])
                    else:
                        self.addCmdLine("%s is not a valid commands. Valid commands and usage:" % cmd_args[1])
                        for line in self.usage.values():
                            self.addCmdLine("\t" + line)
            elif cmd_args[0] == "login":
                if self.current_user is not None:
                    self.addCmdLine("Yo! You are already logged in as %s" % self.current_user.username)
                    return
                username = cmd_args[1]
                users = self.P.list_accounts(username)
                if users == []:
                    self.addCmdLine("Username %s does not exist. Please create a new account." % cmd_args[1])
                else: 
                    user = users[0]
                    self.current_user = LoginUser(user.username, user.u_id)
                    self.addCmdLine("Logged in as %s" % cmd_args[1])
            elif cmd_args[0] == "mk-user":
                if self.current_user is not None:
                    self.addCmdLine("Cannot create a user while logged in")
                    return
                user = self.P.create_account(cmd_args[1])
                if user is not None:
                    self.current_user = LoginUser(cmd_args[1], user.u_id)
                    self.addCmdLine("Created account and logged in as %s" % cmd_args[1])
                else:
                    self.addCmdLine("Could not create account")

            # all following commands must be called while logged in
            elif self.current_user is None:
                self.addCmdLine("Cannot call %s while not logged in" % cmd_args[0])
                return
            elif cmd_args[0] == "ls-groups":
                response = self.P.list_groups() if len(cmd_args) == 1 else self.P.list_groups(cmd_args[1])
                for group in response:
                    self.addCmdLine("Group Name: %s\t Group ID: %d" % (group.g_name, group.g_id))
            elif cmd_args[0] == "ls-users":
                response = self.P.list_accounts() if len(cmd_args) == 1 else self.P.list_accounts(cmd_args[1])
                for user in response:
                    self.addCmdLine("Username: %s\t User ID: %d" % (user.username, user.u_id))
            elif cmd_args[0] == "ls-group-members":
                response = self.P.list_group_members(cmd_args[1])
                for user in response:
                    self.addCmdLine("Username: %s\t User ID: %d" % (user.username, user.u_id))
            elif cmd_args[0] == "mk-group":
                response = self.P.create_group(cmd_args[1])
                if response is not None:
                    self.addCmdLine("Created group %s" % cmd_args[1])
                else:
                    self.addCmdLine("Could not create group: %s" % response)
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
                self.addCmdLine("Logged out of account")
            elif cmd_args[0] == "talk-with":
                tpe = cmd_args[1]
                if tpe != "user" and tpe != "group":
                    self.addCmdLine("Type of conversation must be either user or group.")
                    return
                to_name = cmd_args[2]
                if tpe == "user":
                    convo_id = self.P.create_conversation(self.current_user.username, to_name)
                    self.mode = int(convo_id)
                elif tpe == "group":
                    groups = self.P.list_groups(to_name)
                    if groups == []:
                        self.addCmdLine("Group %s does not exist." % to_name)
                    else:
                        self.mode = int(groups[0].g_id)
                self.display.setLines(self.cmd_history, adjust=True)
