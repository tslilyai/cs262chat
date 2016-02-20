# cs262chat
Chat Application for CS262: Introduction to Distributed Systems

David Ding, Lily Tsai, Dan Fu, Ross Rheingans-Yoo

# Running the Application

To start up a chat server: `python server_main.py [protocol] [port]`

To start up a chat client: `python client_main.py [protocol] [port] [username]`

`protocol` can be one of either `protobuf` or `custom`.

# Client API 

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

