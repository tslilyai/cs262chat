'''
THIS IS A CLIENT-FACING INTERFACE

This defines an abstract protocol class that both communication protocols must implement
Front end calls these function (client-side)
'''

class Message(object):
    def __init__(self, m_id, from_name, to_id, msg):
        self.m_id = m_id
        self.from_name = from_name
        self.to_id = to_id
        self.msg = msg

class Group(object):
    def __init__(self, g_id, gname):
        self.g_id = g_id
        self.gname = gname

class User(object):
    def __init__(self, u_id, username):
        self.u_id = u_id
        self.username = username

class Protocol(object):
    '''An abstract class representing a protocol'''
    def __init__(self, port):
        raise NotImplementedError

    # RUN
    def client_run(self, port="8080"):
        raise NotImplementedError

    ''' 
    MESSAGING 
    '''
    def send_message(self, from_name, dest_id, msg):
        '''Returns None on success, or an error string'''
        raise NotImplementedError
    
    # returns a list of (from, msg) string tuples
    def fetch_messages(self, to_id, checkpoint=0):
        '''Returns a list of Messages addressed to to_id'''
        raise NotImplementedError

    '''
    CREATION AND DELETION 
    '''
    # only creates an empty group
    # returns a group object
    def create_group(self, groupname=""):
        raise NotImplementedError
    
    # returns a success or error message string
    # returns a user object
    def create_account(self, username=""):
        raise NotImplementedError
    
    # returns a success or error message string
    def remove_account(self, username=""):
        raise NotImplementedError

    '''
    GROUPS 
    '''
    # returns a success or error message string
    def edit_group_name(self, old_name="", new_name=""):
        raise NotImplementedError
    
    # returns a success or error message string
    def remove_group_member(self, groupname="", membername=""):
        raise NotImplementedError
   
   # returns a success or error message string
    def add_group_member(self, groupname="", membername=""):
        raise NotImplementedError

    # LISTING 
    # returns a list of tuples (name, id)
    def list_groups(self, pattern="%"):
        raise NotImplementedError
    def list_accounts(self, pattern="%"):
        raise NotImplementedError
    def list_group_members(self, groupname=""):
        raise NotImplementedError
