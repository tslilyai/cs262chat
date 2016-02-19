'''
THIS IS A CLIENT-FACING INTERFACE

This defines an abstract protocol class that both communication protocols must implement
Front end calls these function (client-side)
'''

class Protocol(object):
    def __init__(self, protocol):
        self.P = protocol

    # RUN
    def client_run(self, username, port):
        self.P.client_run(username, port)

    ''' 
    MESSAGING 
    '''
    # returns a success or error message string
    def send_individual_message(self, src="", dest="", msg=""):
        if src == "" or dest == "" or msg == "":
            return "please provide a source username, destination uesrname, and message"
        return self.P.send_individual_message(src, dest, msg);
    
    # returns a success or error message string
    def send_group_message(self, src="", dest="", msg=""):
        if src == "" or dest == "" or msg == "":
            return "please provide a source username, destination uesrname, and message"
        return self.P.send_group_message(src, dest, msg);
    
    # returns a list of (from, msg) string tuples
    def get_messages(self, dest=""):
        if dest == "":
            return "please provide a destination username"
        self.P.get_messages(src, dest, msg);

    '''
    CREATION AND DELETION 
    '''
    # returns a success or error message string
    # only creates an empty group
    def create_group(self, groupname=""):
        if groupname == "":
            return "please provide a groupname"
    
    # returns a success or error message string
    def create_account(self, username=""):
        if username == "":
            return "please provide a username"
    
    # returns a success or error message string
    def remove_account(self, username=""):
        if username == "":
            return "please provide a username"

    '''
    GROUPS 
    '''
    # returns a success or error message string
    def edit_group_name(self, old_name="", new_name=""):
        if old_name == "" or new_name == "":
            return "please provide the old and new group names"
    
    # returns a success or error message string
    def remove_group_member(self, groupname="", membername=""):
        if groupname == "" or membername == "":
            return "please provide a group name and member name"
   
   # returns a success or error message string
    def add_group_member(self, groupname="", membername=""):
        if groupname == "" or membername == "":
            return "please provide a group name and member name"

    # LISTING 
    # returns a list of strings
    def list_groups(self, pattern="%"):
    def list_accounts(self, pattern="%"):
    def list_group_members(self, groupname=""):
