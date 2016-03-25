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
    A Group defines a group object, which consists of a
    group identifier and group name.
    
    A group in the database consists of several users.
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
    A User defines a user object, which consists of a user 
    identifier and a username.

    A user object is used to give identities to
    individuals using the client application.
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
    Protocol is an abstract class representing the API the client
    application calls to communicate to the server and other clients.

    Each type of communication protocol (for example, REST or protobufs) must 
    implement this API in order for the application to use the protocol.
    '''
    def __init__(self, host, port):
        '''
        Initialize a Protocol object
        :param host: string identifier for the server (server name or IP address)
        :param port: string identifying which port to communicate over 
        :return: a Protocol object 
        '''
        raise NotImplementedError

    ''' 
    MESSAGING 
    '''
    def send_message(self, from_name, dest_id, msg):
        '''
        Send a message to another user
        :param from_name: string specifying the name of the user who is sending the message
        :param dest_id: integer uniquely identifying the destination user
        :return: None on success, or an error string
        '''
        raise NotImplementedError
    
    def fetch_messages(self, to_id, checkpoint=0):
        '''
        Fetch all messages for a user (past a certain checkpoint). The checkpoint 
        corresponds to a message identifier; only messages with identifiers greater
        than the checkpoint are fetched.

        :param to_id: integer uniquely identifying the user who is fetching messages
        :param checkpoint: integer specifying which messages should be fetched (only messages with m_id > checkpoint)
        :return: list of Message objects
        '''
        raise NotImplementedError

    '''
    CREATION AND DELETION 
    '''
    def create_group(self, g_name=""):
        '''
        Create a group with the specified name. The name must be unique from
        all other groups.
        
        :param g_name: string uniquely identifying the group to create
        :return: Group object with the group name assigned to g_name
        '''
        raise NotImplementedError
    
    def create_account(self, username=""):
        '''
        Create a user with the specified name. The name must be unique from
        all other users.
        
        :param username: string uniquely identifying the user to create
        :return: User object with the user's name assigned t username 
        '''
        raise NotImplementedError
    
    def remove_account(self, username=""):
        '''
        Removes the user with the specified name.
        
        :param username: string uniquely identifying the user to remove
        :return: None on success, or an error string
        '''
        raise NotImplementedError

    '''
    GROUPS 
    '''
    def edit_group_name(self, old_name="", new_name=""):
        '''
        Changes the group with name "old_name" to "new_name", where "new_name"
        is unique from all other groups.
        
        :param old_name: string uniquely identifying the group 
        :param new_name: string of the new name that will uniquely identifying the group 
        :return: None on success, or an error string
        '''
        raise NotImplementedError
    
    def remove_group_member(self, g_name="", membername=""):
        '''
        Removes the specified user from the specified group.
        
        :param g_name: string uniquely identifying the group 
        :param membername: string uniquely identifying the user to remove
        :return: None on success, or an error string
        '''
        raise NotImplementedError
   
    def add_group_member(self, g_name="", membername=""):
        '''
        Adds the specified user to the specified group.
        
        :param g_name: string uniquely identifying the group 
        :param membername: string uniquely identifying the user to add
        :return: None on success, or an error string
        '''
        raise NotImplementedError

    '''
    Listing 
    '''
    def list_groups(self, pattern="%"):
        '''
        Returns all the groups whose names match the specified pattern. 
        
        :param pattern: string that pattern matches (using the specified pattern matching language described in the higher-level documentation) the names of the groups to list.
        :return: a list of Group objects (empty list if none match)
        '''
        raise NotImplementedError
    def list_accounts(self, pattern="%"):
        '''
        Returns all the users whose names match the specified pattern.
        
        :param pattern: string that pattern matches (using the specified pattern matching language described in the higher-level documentation) the names of the users to list.
        :return: a list of User objects (empty list if none match)
        '''
        raise NotImplementedError
    def list_group_members(self, g_name=""):
        '''
        Returns all the users in the specified group.
        
        :param g_name: string uniquely identifying the group 
        :return: a list of User objects (empty list if none match)
        '''
        raise NotImplementedError
