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
from protocols import Protocol
from collections import defaultdict
from window.cmd_mode import CmdWindow
#from window.convo_mode import ConvoWindow

def poll_for_messages(group_id, p, delay):
    messages = defaultdict(list)
    try:
        while(1):
            time.sleep(delay)
            msgs = p.fetch_messages(group_id)
            # not logged in yet, just keep looping 
            if msgs[0][0] == None:
                # print on screen "not logged in, no messages"
                continue
            else:
                for m in msgs:
                    messages[m.group_id].append(m)
    except KeyboardInterrupt:
        exit(0)

def main(screen):
    protocol = sys.argv[1]
    port = sys.argv[2]
    p = Protocol(protocol)
    
    cmd_window = CmdWindow(screen, p)
#    conversation_window = ConvoWindow(screen, p)

    try:
        p.client_run()
        while(1):
            group_id = cmd_window.run()
            conversation_window.enter_convo_mode(group_or_user_id)
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print "Error running client: %s" % e

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
