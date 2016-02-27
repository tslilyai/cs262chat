'''
The main function to start and run the client lives here!

The front end will consist of a portion that shows all incoming messages (RHS of console) and a portion that acts as a command-line interface, accepting commands.

The user can also enter "conversation thread mode," which transforms the command-line interface into a chat box with another user or group.

Login and Account Creation: These must be called without being logged in.

    > login [name]
    > mk-user [name]

Command Mode: These cannot be called without being logged in

    > ls_groups [pattern (optional)]
    > ls-users [pattern (optional)]
    > ls-group-members [name] [pattern (optional)]
    > mk-group [name] [users]
    > send-msg [dest-name] [message]
    > fetch-msgs [id]
    > logout

Conversation Thread Mode
Running `> enter-thread [groupname/username]` enters "conversation mode," in which you can send messages to a group or individual user simply by typing and pressing enter.

Escape thread mode back to command mode simply by typing ESC.
'''

import sys
import os
import curses
import curses.textpad
import thread
import time

from protobuf.protobuf_wrapper import Protobuf_Protocol
from collections import defaultdict
from window.window import Application


def main(screen):
    protocol = sys.argv[1]
    port = sys.argv[2]
    if protocol == 'protobuf':
        p = Protobuf_Protocol(int(port))

    window = Application(screen, p)
    window.run()    

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
