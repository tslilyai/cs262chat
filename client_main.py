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
    > fetch-msgs
    > logout

Conversation Thread Mode
Running `> enter-thread [groupname/username]` enters "conversation mode," in which you can send messages to a group or individual user simply by typing and pressing enter.

Escape thread mode back to command mode simply by typing ESC.
'''

import sys
import thread
import time
from protocols import Protocol
from collections import defaultdict

def display_messages():


def poll_for_messages(p, delay):
    messages = defaultdict(list)
    try:
        while(1):
            time.sleep(delay)
            msgs = p.fetch_messages()
            # not logged in yet, just keep looping 
            if msgs[0][0] == None:
                # print on screen "not logged in, no messages"
                continue
            else:
                for m in msgs:
                    messages[m.from_id].append(m)
    except KeyboardInterrupt:
        exit(0)

def main():
    protocol = sys.argv[1]
    port = sys.argv[2]
    p = Protocol(protocol)

    try:
        p.client_run()
        thread.start_new_thread(poll_for_messages, (p, 1,))
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print "Unable to start thread to get messages: %s" % e

'''
    # do fancy setup stuff here to enter "command mode" and set up UI 

    while(1):
        # read from console, run cmd (using p) and handle output appropriately
        
        # poll server for new messages and display on RHS of screen
        p.get_messages(username)
'''

if __name__ == "__main__":
    main()
