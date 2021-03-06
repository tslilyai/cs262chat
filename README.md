# cs262chat
Chat Application for CS262: Introduction to Distributed Systems

David Ding, Lily Tsai, Dan Fu, Ross Rheingans-Yoo

# Running the Application
To install on Ubuntu, `install.sh` may prove handy (the install script is not well tested). To run: `source install.sh`

We support two types of communication protocols: `protocol` can be one of either `protobuf` or `custom`.

- To start up a chat server: `python server_main.py [--protocol protocol] [--port port]`

- To start up a chat client (logged in as user `username`): `python client_main.py [--protocol protocol] [--port port] [--host host]`

Before running the application, you will need to initialize the database.  This can be done using `python db.py init`.  To start out with some test users/groups, call `python db.py test`.  To remove all users, groups, and messages, call `python db.py clean`.

# Front End 

The front end is a curses app that allow the user to interface with the server. There are two modes of operation for the front-end. In command mode, the user types in a command, and when the user types enter, the command is interpreted as a command and executed. In conversation mode, the user types in a message, and when the user types enter, the message is sent to the recipient. The application starts in command mode. To enter conversation mode, the user issues the command `talk-with [user|group] [username|groupname]`. To enter command mode from conversation mode, the user presses ESC.

The application could either be logged-in or not logged in. If the application is not logged in, the only valid commands are the `login` and `create-account` commands. If the application is logged in, the user can log out via the `logout` command or `remove-account` command. A global variable, `current_user`, keeps track of the current user, and is equal to None if the application is not logged in. The `current_user` object has fields `username`, `user_id`, `checkpoint`, and `messages`, where checkpoint is the last message id fetched for this user and messages is a dictionary mapping from conversation id to a list of messages..

The login command takes a username as argument. The client executes a `list_user(username)` RPC-call to the server, which returns the user id and username of the specified username (if the user exists; otherwise, it returns an empty list). The client then records the id and username in the `current_user` global variable.

Upon application start, a fetch thread is spawned. This thread sleeps as long as `current_user` is None. If the application is logged in, the thread periodically calls `get_messages(current_user.id, checkpoint)` to get a list of messages for the `current_user` with message ids greater than checkpoint. The thread adds each method to `current_user.messages`, using the `to_id` of the message as the conversation id.

The GUI itself consists of two windows, the display window, and input window, along with a controller for both windows. The input window has a buffer, which keeps track of all the characters that have been inputted since the last ENTER. The controller has a run function, which polls for user keystroke inputs, and based on the inputs, perform certain actions. The UP and DOWN arrow keys scrolls the display window, the ESC key switches to command mode if the current mode is not command mode, the ENTER key causes the input window's buffer to be interpreted and clears that buffer, and all other keys cause the corresponding characters to be appended to the input window's buffer. The controller stores a variable keeping track of the mode (command mode or conversation mode). The mode is an integer equal to -1 for command mode, and nonnegative for conversation mode, with the value equal to the conversation id.

Interpretation of the input window buffer differs between command mode and conversation mode. In command mode, the command is first appended to the controller's `command_history` array, and the string [PROMPT]+command is appended to the controller's `command_mode_output` array.    The command is then parsed and some action is performed. Then, the output of that command is appended to the `command_mode_output` array. In conversation mode, the buffer is sent to the server via the RPC call `send_message(from_id=current_user.id, to_id=controller.mode, msg=inputw.buffer)`. 

The display window holds a list of lines and a cursor variable, which stores the line number of the top most line in the screen. This cursor is changed when the user scrolls using the UP and DOWN keys. It provides functions `set_lines()` and `render()`. Render simply prints the lines from cursor to `cursor+window_height`. Set lines sets the lines variable of the display and sets the cursor to 0. When the controller enters command mode (`switch_to_command_mode`), it calls the `display.set_lines` function on `controller.command_mode_output` array. When the controller enters conversation mode (`switch_to_convo_mode`), it calls the `display_set_lines` function on `current_user.messages[controller.mode]`.

In command mode, the display render function is called on ENTER key press and after the command output has been appended to the `command_mode_output` array. In conversation mode, the render function is called in the fetch messages thread if one of the fetched messages has `to_id` equal to controller.mode, after all messages in this round has been processed.

Most commands in command mode are the same as the RPC calls. The special ones are list-conversations and `talk-with [user|group] [username|groupname]`. `list-conversations` lists all conversations for which the user has pending messages (i.e., all entries of `current_user.messages`). `talk-with [user|group] [username|groupname]` switches to conversation mode. This command works as follows: for groups, talk-with first sends a `list_group` query to the server to grab the group id of the specified group name, sets controller.mode to equal the group id, and calls `switch_to_convo_mode`. For users, talk-with sends a `get_or_create_vgroup_id` query to the server to either create a virtual group, or return an existing virtual group id. This id is returned, and we set controller.mode to equal this id and call `switch_to_convo_mode`.

Running `> enter-thread [groupname/username]` enters "conversation mode," in which you can send messages to a group or individual user simply by typing and pressing enter.

Escape thread mode back to command mode simply by typing ESC.

### Commands

    > login [username]
    > mk-user [username]
    > delete-account
    > ls-groups [pattern (optional)]*
    > ls-users [pattern (optional)]*
    > ls-group-members [groupname]*
    > mk-group [groupname]*
    > add-group-member [groupname] [username]*
    > remove-group-member [groupname] [username]*
    > talk-with [group/user] [group or user name]*
    > logout*
    
    *must be logged in

### Patterns

A highly sophisticated pattern matching language:

	% matches 0 or more characters
	_ matches exactly one character
	[charset] matches sets or ranges of characters
	[^charset] matches the complement of a set or range of characters

Coincidentally, this language is also used in the SQL like query: http://www.w3schools.com/sql/sql_wildcards.asp. And when you sanitize SQL queries, these strings are unmodified.

# Communication Protocols API
This interface should be implemented by any protocol used by the chat server.

    def client_run(port)

### MESSAGING 
    def send_message(self, from_name, dest_id, msg):
        '''Returns None on success, or an error string'''
    
    def fetch_messages(self, to_id, checkpoint=0):
        '''Returns a list of Messages addressed to to_id'''
        
###CREATION AND DELETION 
    
    def create_group(self, g_name=""):
        '''Returns a Group object with g_name=g_name'''
    
    def create_account(self, username=""):
        '''Returns a User object with username=username'''
    
    def remove_account(self, username=""):
        '''Returns None or error string'''

###GROUPS 
    
    def edit_group_name(self, old_name="", new_name=""):
        '''Returns None or error string'''
    
    def remove_group_member(self, g_name="", membername=""):
        '''Returns None or error string'''
   
    def add_group_member(self, g_name="", membername=""):
        '''Returns None or error string'''

### LISTING 
    
    def list_groups(self, pattern="%"):
        '''Returns a list of Group objects (empty list if none match)'''
    
    def list_accounts(self, pattern="%"):
        '''Returns a list of User objects (empty list if none match)'''
   
    def list_group_members(self, g_name=""):
        '''Returns a list of User objects (empty list if none)'''

# Database API 
        void create_tables(self): creates database tables for the app
        
        int get_or_create_vgid(self, int to_id, int from_id):
            returns the vgroup id for users to_id and from_id. Creates vgroup if it doesn't exist.
        
        void insert_message(int to_id, int from_id, string msg):
            creates a new message from from_id to to_id with content msg.
            from_id is the id of a user.
            to_id is the id of a group or vgroup.
        
        int get_user_id(string u_name):
            returns the user id for user with username u_name
        
        int get_group_id(string g_name):
            returns the group id for group with name g_name
        
        messages[] get_messages(int u_id, int checkpoint):
            returns a list of dictionaries representing messages (fields m_id, to_id, from_name, msg)
            that the user with id u_id could see.
            All returned messages have id greater than checkpoint.
        
        void create_group(string g_name):
            creates a group with name g_name.
        
        void create_account(string u_name):
            creates a new user with username u_name
        
        void add_group_member(string g_name, string u_name):
            adds user with username u_name to group with name g_name
        
        void remove_account(string u_name):
            Delete user with username u_name
        
        void remove_group_member(string g_name, string u_name):
            Delete user with username u_name from group with name g_name
        
        void edit_group_name(string name, string newname):
            changes name of group with name g_name to newname
        
        list(group) get_groups(string pattern):
            returns a list of groups whose names matches pattern.
            pattern is specified in SQL pattern syntax.
        
        list(user) get_accounts(string pattern):
            returns a list of users whose usernames matches pattern.
            pattern is specified in SQL pattern syntax.
        
        list(user) get_group_members(string g_name):
            returns a list of users belong to group with name g_name
        
