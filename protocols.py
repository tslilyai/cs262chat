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
    def send_message(self, src, dest, msg):
        self.P.send_message(src, dest, msg);

    def get_messages(self, dest):

    # CREATION AND DELETION 
    def create_group(self, groupname):
    def create_account(self, username):
    def remove_account(self):

    # GROUPS 
    def edit_group_name(self, old_name, new_name):
    def remove_group_member(self, groupname, member):
    def add_group_member(self, groupname, member):

    # LISTING 
    def list_groups(self, pattern):
    def list_accounts(self, pattern):
    def list_group_members(self, groupname):
