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
    def __init__(self, g_id, g_name):
        self.g_id = g_id
        self.g_name = g_name

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
    
    def fetch_messages(self, to_id, checkpoint=0):
        '''Returns a list of Messages addressed to to_id'''
        raise NotImplementedError

    '''
    CREATION AND DELETION 
    '''
    def create_group(self, g_name=""):
        '''Returns a Group object with g_name=g_name'''
        raise NotImplementedError
    
    def create_account(self, username=""):
        '''Returns a User object with username=username'''
        raise NotImplementedError
    
    def remove_account(self, username=""):
        '''Returns None or error string'''
        raise NotImplementedError

    '''
    GROUPS 
    '''
    def edit_group_name(self, old_name="", new_name=""):
        '''Returns None or error string'''
        raise NotImplementedError
    
    def remove_group_member(self, g_name="", membername=""):
        '''Returns None or error string'''
        raise NotImplementedError
   
    def add_group_member(self, g_name="", membername=""):
        '''Returns None or error string'''
        raise NotImplementedError

    '''
    Listing 
    '''
    def list_groups(self, pattern="%"):
        '''Returns a list of Group objects (empty list if none match)'''
        raise NotImplementedError
    def list_accounts(self, pattern="%"):
        '''Returns a list of User objects (empty list if none match)'''
        raise NotImplementedError
    def list_group_members(self, g_name=""):
        '''Returns a list of User objects (empty list if none)'''
        raise NotImplementedError
