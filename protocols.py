'''
protocols.py defines three classes, Message, Group, User, and Protocol. 

Protocol is an abstract protocol class that exposes the client API for communicating
to the server and other clients. 

Message/Group/User objects are passed around and returned by the Protocol methods.

Both communication protocols must implement this class.
'''

class Message(object):
    '''
    Message defines a message object, consisting of a 
    message id, name of sender, identifier of the 
    recipient, and the message itself.

    Messages are the objects used to send and receive messages 
    within the client protocols.
    '''
    def __init__(self, m_id, from_name, to_id, msg):
        '''
        Initialize a Message object
        :param m_id: integer uniquely identifying the message
        :param from_name: string representing the name of the sender of the message
        :param to_id: integer uniquely identifying the recipient of the message 
        :param msg: string representing the message text
        :return: an initialized Message object
        '''
        self.m_id = m_id
        self.from_name = from_name
        self.to_id = to_id
        self.msg = msg

class Group(object):
    '''
    Group
    '''
    def __init__(self, g_id, g_name):
        '''
        Initialize a Group
        :param g_id: integer uniquely identifying the group
        :param g_name: string representing the name of the group 
        :return: an initialized Group object
        '''
        self.g_id = g_id
        self.g_name = g_name

class User(object):
    '''
    User
    '''
    def __init__(self, u_id, username):
        '''
        Initialize a User object
        :param u_id: integer uniquely identifying the user
        :param username: string representing the name of the user
        :return: an initialized User object
        '''
        self.u_id = u_id
        self.username = username

class Protocol(object):
    '''
    Protocol is an abstract class representing a protocol
    '''
    def __init__(self, host, port):
        raise NotImplementedError

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
