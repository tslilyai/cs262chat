'''
THIS IS A CLIENT-FACING INTERFACE

This defines an abstract protocol class that both communication protocols must implement
Front end calls these function (client-side)
'''

class Protocol(object):
    def __init__(self, protocol):
        self.P = protocol

    # RUN
    def client_run(self, port):

    # MESSAGING 
    # returns a success or error message string
    def send_message(self, src, dest, msg):
        self.P.send_message(src, dest, msg);

    # returns a list of (from, msg) string tuples
    def get_messages(self, dest):

    # CREATION AND DELETION 
    # returns a success or error message string
    def create_group(self, groupname):
    # returns a success or error message string
    def create_account(self, username):
    # returns a success or error message string
    def remove_account(self):

    # GROUPS 
    # returns a success or error message string
    def edit_group_name(self, old_name, new_name):
    # returns a success or error message string
    def remove_group_member(self, groupname, member):
    # returns a success or error message string
    def add_group_member(self, groupname, member):

    # LISTING 
    # returns a list of strings
    def list_groups(self, pattern):
    def list_accounts(self, pattern):
    def list_group_members(self, groupname):
