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
from protocols import Protocol

def main():
    protocol = sys.argv[1]
    port = sys.argv[2]
    p = Protocol(protocol)

    p.client_run("fding", port)
    p.fetch_messages()
'''
    # do fancy setup stuff here to enter "command mode" and set up UI 

    while(1):
        # read from console, run cmd (using p) and handle output appropriately
        
        # poll server for new messages and display on RHS of screen
        p.get_messages(username)
'''

if __name__ == "__main__":
    main()
