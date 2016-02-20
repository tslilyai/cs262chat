# cs262chat
Chat Application for CS262: Introduction to Distributed Systems

David Ding, Lily Tsai, Dan Fu, Ross Rheingans-Yoo

# Running the Application
We support two types of communication protocols: `protocol` can be one of either `protobuf` or `custom`.

- To start up a chat server: `python server_main.py [protocol] [port]`

- To start up a chat client (logged in as user `username`): `python client_main.py [protocol] [port]`


# Client API 
The front end will consist of a portion that shows all incoming messages (RHS of console) and a portion that acts as a command-line interface, accepting commands.

The user can also enter "conversation thread mode," which transforms the command-line interface into a chat box with another user or group.

### Login and Account Creation
These must be called without being logged in.

    > login [name]
    > mk-user [name]

### Command Mode
These cannot be called without being logged in

    > ls_groups [pattern (optional)]
    > ls-users [pattern (optional)]
    > ls-group-members [name] [pattern (optional)]
    > mk-group [name] [users]
    > send-msg [dest-name] [message]
    > fetch-msgs
    > logout

### Conversation Thread Mode
Running `> enter-thread [groupname/username]` enters "conversation mode," in which you can send messages to a group or individual user simply by typing and pressing enter.

Escape thread mode back to command mode simply by typing ESC.

# Communication Protocol API
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
    def create_account(self, username=""):
    
    # returns a success or error message string
    def remove_account(self, username=""):

###GROUPS 
    
    # returns a success or error message string
    def edit_group_name(self, old_name="", new_name="")
    # returns a success or error message string
    def remove_group_member(self, groupname="", membername="")
    # returns a success or error message string
    def add_group_member(self, groupname="", membername="")

### LISTING 
    
    # returns a list of strings
    def list_groups(self, pattern="%"):
    def list_accounts(self, pattern="%"):
    def list_group_members(self, groupname=""):


# Database API 

