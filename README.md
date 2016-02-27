# cs262chat
Chat Application for CS262: Introduction to Distributed Systems

David Ding, Lily Tsai, Dan Fu, Ross Rheingans-Yoo

# Running the Application
We support two types of communication protocols: `protocol` can be one of either `protobuf` or `custom`.

- To start up a chat server: `python server_main.py [protocol] [port]`

- To start up a chat client (logged in as user `username`): `python client_main.py [protocol] [port]`


# Front End 

The front end is a curses app that allow the user to interface with the server. There are two modes of operation for the front-end. In command mode, the user types in a command, and when the user types enter, the command is interpreted as a command and executed. In conversation mode, the user types in a message, and when the user types enter, the message is sent to the recipient. The application starts in command mode. To enter conversation mode, the user issues the command “talk-with [user|group] [username|groupname]. To enter command mode from conversation mode, the user presses ESC.

The application could either be logged-in or not logged in. If the application is not logged in, the only valid command is the “login” and “create-account” command. If the application is logged in, the user can log out via the “logout” command or “remove-account” command. A global variable, current_user, keeps track of the current user, and is equal to None if the application is not logged in. The current_user object has fields username, user_id, checkpoint, and messages, where checkpoint is the last message id fetched for this user and messages is a dictionary mapping from conversation id to a list of messages..

The login command takes a username as argument. The client executes a list_user(username) RPC-call to the server, which returns the user id and username of the specified username (if the user exists; otherwise, it returns an empty list). The client then records the id and username in the current_user global variable.

Upon application start, a fetch thread is spawned. This thread sleeps as long as current_user is None. If the application is logged in, the thread periodically calls get_messages(current_user.id, checkpoint) to get a list of messages for the current_user with message ids greater than checkpoint. The thread adds each method to current_user.messages, using the to_id of the message as the conversation id.

The GUI itself consists of two windows, the display window, and input window, along with a controller for both windows. The input window has a buffer, which keeps track of all the characters that have been inputted since the last ENTER. The controller has a run function, which polls for user keystroke inputs, and based on the inputs, perform certain actions. The UP and DOWN arrow keys scrolls the display window, the ESC key switches to command mode if the current mode is not command mode, the ENTER key causes the input window’s buffer to be interpreted and clears that buffer, and all other keys cause the corresponding characters to be appended to the input window’s buffer. The controller stores a variable keeping track of the mode (command mode or conversation mode). The mode is an integer equal to -1 for command mode, and nonnegative for conversation mode, with the value equal to the conversation id.

Interpretation of the input window buffer differs between command mode and conversation mode. In command mode, the command is first appended to the controller’s command_history array, and the string [PROMPT]+command is appended to the controller’s command_mode_output array.    The command is then parsed and some action is performed. Then, the output of that command is appended to the command_mode_output array. In conversation mode, the buffer is sent to the server via the RPC call send_message(from_id=current_user.id, to_id=controller.mode, msg=inputw.buffer). 

The display window holds a list of lines and a cursor variable, which stores the line number of the top most line in the screen. This cursor is changed when the user scrolls using the UP and DOWN keys. It provides functions set_lines() and render(). Render simply prints the lines from cursor to cursor+window_height. Set lines sets the lines variable of the display and sets the cursor to 0. When the controller enters command mode (switch_to_command_mode), it calls the display.set_lines function on controller.command_mode_output array. When the controller enters conversation mode (switch_to_convo_mode), it calls the display_set_lines function on current_user.messages[controller.mode].

In command mode, the display render function is called on ENTER key press and after the command output has been appended to the command_mode_output array. In conversation mode, the render function is called in the fetch messages thread if one of the fetched messages has to_id equal to controller.mode, after all messages in this round has been processed.

Most commands in command mode are the same as the RPC calls. The special ones are list-conversations and talk-with [user|group] [username|groupname]. list-conversations lists all conversations for which the user has pending messages (i.e., all entries of current_user.messages). talk-with [user|group] [username|groupname] switches to conversation mode. This command works as follows: for groups, talk-with first sends a list_group query to the server to grab the group id of the specified group name, sets controller.mode to equal the group id, and calls switch_to_convo_mode. For users, talk-with sends a get_or_create_vgroup_id query to the server to either create a virtual group, or return an existing virtual group id. This id is returned, and we set controller.mode to equal this id and call switch_to_convo_mode.

Running `> enter-thread [groupname/username]` enters "conversation mode," in which you can send messages to a group or individual user simply by typing and pressing enter.

Escape thread mode back to command mode simply by typing ESC.

### Commands

    > login [username]
    > mk-user [username]
    > ls-groups [pattern (optional)]*
    > ls-users [pattern (optional)]*
    > ls-group-members [groupname]*
    > mk-group [groupname]*
    > add-group-member [groupname] [username]*
    > remove-group-member [groupname] [username]*
    > talk-with [group/user] [group or user name]*
    > logout*
    
    *must be logged in

# Communication Protocols API
This interface should be implemented by any protocol used by the chat server.

    def client_run(username, port)

### MESSAGING 
    
    # returns a success or error message string
    def send_individual_message(self, src="", dest="", msg="")
    
    # returns a success or error message string
    def send_group_message(self, src="", dest="", msg="")
    
    # returns a list of (from, msg) string tuples
    def get_messages(self, dest="")

###CREATION AND DELETION 
    
    # returns a success or error message string
    # only creates an empty group
    def create_group(self, groupname="")
    
    # returns a success or error message string
    def create_account(self, username="")
    
    # returns a success or error message string
    def remove_account(self, username="")

###GROUPS 
    
    # returns a success or error message string
    def edit_group_name(self, old_name="", new_name="")
    # returns a success or error message string
    def remove_group_member(self, groupname="", membername="")
    # returns a success or error message string
    def add_group_member(self, groupname="", membername="")

### LISTING 
    
    # returns a list of string
    def list_groups(self, pattern="%")
    def list_accounts(self, pattern="%")
    def list_group_members(self, groupname="")


# Database API 
    def create_tables(self)
    def insert_message(self, to_id, from_id, msg)
    def get_user_id(self, uname)
    def get_group_id(self, gname)
    def get_messages(self, u_id)
    def create_group(self, gname)
    def create_account(self, uname)
    def add_group_member(self, gname, uname)
    def remove_account(self, uname)

