'''
THIS IS A CLIENT-FACING INTERFACE

This defines an abstract protocol class that both communication protocols must implement
Front end calls these function (client-side)
'''

from protobuf.protobuf_wrapper import Protobuf_Protocol

class Protocol(object):
    def __init__(self, protocol):
        if protocol == "protobuf":
            self.P = Protobuf_Protocol()

    # RUN
    def client_run(self, username, port):
        self.P.client_run(username, int(port))
        self.username = username
        print "client running"

    ''' 
    MESSAGING 
    '''
    # returns a success or error message string
    def send_individual_message(self, dest="", msg=""):
        if dest == "" or msg == "":
            return "please provide a source username, destination uesrname, and message"
        return self.P.send_individual_message(self.username, dest, msg);
    
    # returns a success or error message string
    def send_group_message(self, dest="", msg=""):
        if src == "" or dest == "" or msg == "":
            return "please provide a destination username, and message"
        return self.P.send_group_message(self.username, dest, msg);
    
    # returns a list of (from, msg) string tuples
    def fetch_messages(self):
        msgs = (self.P.fetch_messages())
        print "fetched messages"
        for m in msg:
            print m

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
        self.P.list_groups(pattern)
    def list_accounts(self, pattern="%"):
        self.P.list_acocunts(pattern)
    def list_group_members(self, groupname=""):
        self.P.list_group_members(pattern)
