'''
This class implements the interface defined in protocols.py
for a custom wire protocol
'''

from protocols import Protocol, Message, User, Group
import requests
import json

_VERSION_NUMBER = '1.0'
_TIMEOUT_SECONDS = 30

class TimeoutResponse:
    def __init__(self):
        self.status_code = requests.codes.not_found

class CustomProtocol(Protocol):
    '''
    CustomProtocol implements the abstract Protocol class (protocols.py).
    
    All functions behave as specified in the documentation for the Protocol class

    How to make requests:
    
    Create an object with self.__create_object:
        action is necessary
        actor, setting, target, value change depending on method, but do
            what makes sense
        look at comments if something is unclear
    Dump the object to JSON
    Pass the JSON dump to either __send_get or __send_post
    Pass that to __get_response when necessary
    '''

    def __get_response(self, response):
        if response.status_code != requests.codes.ok:
            return "Error: %s" % response.text
        else: 
            return None
    
    def __create_object(self, action, actor=None, setting=None, target=None, value=None):
        ret = {}
        ret['action'] = action
        ret['version'] = _VERSION_NUMBER
        if actor != None:
            ret['actor'] = actor
        if setting != None:
            ret['setting'] = setting
        if target != None:
            ret['target'] = target
        if value != None:
            ret['value'] = value
        return ret
            
    def __send_get(self, params):
        try:
            return requests.get(self.url, params=params, timeout=_TIMEOUT_SECONDS)
        except Exception as e:
            return TimeoutResponse()
    
    def __send_post(self, payload):
        try:
            return requests.post(self.url, json.dumps(payload), timeout=_TIMEOUT_SECONDS)
        except Exception as e:
            print str(e)
            return TimeoutResponse()

    # RUN
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://' + host + ':' + str(port)

    # MESSAGING
    
    # action: message-send, actor: from_id, target: dest_id, value: msg
    def send_message(self, from_name, dest_id, msg):
        payload = self.__create_object('message-send', actor=from_name, target=dest_id, value=msg)
        return self.__get_response(self.__send_post(payload))

    # action: messages-fetch, actor: to_id, setting: checkpoint
    # expects an array that looks like this:
    #   [ { m_id, from_name, to_id, msg }, ... ]
    def fetch_messages(self, to_id, checkpoint=0):
        payload = self.__create_object('messages-fetch', actor=to_id, setting=checkpoint)
        response = self.__send_get(payload)
        #response = TimeoutResponse()
        messages = []
        if response.status_code == requests.codes.ok:
            messages = response.json()
        return [Message(m['m_id'], m['from_name'], m['to_id'], m['msg']) for m in messages]

    # action: conversation-create, actor: username1, target: username2
    # expects a { g_id: g_id } object back, g_id = 0 means something went wrong
    def create_conversation(self, username1, username2):
        payload = self.__create_object('conversation-create', actor=username1, target=username2)
        response = self.__send_post(payload)
        if response.status_code == requests.codes.ok:
            return response.json()['g_id']
        else:
            return None

    # CREATION AND DELETION 
    
    # action: group-create, value: groupname
    # expects a { g_id: g_id, g_name: g_name } object back
    def create_group(self, groupname):
        payload = self.__create_object('group-create', value=groupname)
        response = self.__send_post(payload)
        if response.status_code == requests.codes.ok:
            new_group = response.json()
            if new_group['g_id'] != 0:
                return Group(new_group['g_id'], new_group['g_name'])
        return None
        
    # action: account-create, value: username
    # expects a { username, u_id } object back
    def create_account(self, username):
        payload = self.__create_object('account-create', value=username)
        response = self.__send_post(payload)
        if response.status_code == requests.codes.ok:
            new_user = response.json()
            if new_user['u_id'] != 0:
                return User(new_user['u_id'], new_user['username'])
        return None
    
    # action: account-remove, value: username
    def remove_account(self, username):
        payload = self.__create_object('account-remove', value=username)
        return self.__get_response(self.__send_post(payload))

    # GROUPS
    
    # action: group-edit-name, target: old_name, value: new_name
    def edit_group_name(self, old_name, new_name):
        payload = self.__create_object('group-name-edit', target=old_name, value=new_name)
        return self.__get_response(self.__send_post(payload))
        
    # action: group-edit-name, target: groupname, value: member
    def remove_group_member(self, groupname, member):
        payload = self.__create_object('group-member-remove', target=groupname, value=member)
        return self.__get_response(self.__send_post(payload))
        
    # action: group-edit-name, target: groupname, value: member
    def add_group_member(self, groupname, member):
        payload = self.__create_object('group-member-add', target=groupname, value=member)
        return self.__get_response(self.__send_post(payload))

    # LISTING 
    
    # action: groups-list, setting: pattern
    # expects an array that looks like this:
    #   [ { g_id, g_name }, ... ]
    def list_groups(self, pattern='%'):
        payload = self.__create_object('groups-list', setting=pattern)
        response = self.__send_get(payload)
        groups = []
        if response.status_code == requests.codes.ok:
            groups = response.json()
        return [Group(g['g_id'], g['g_name']) for g in groups]
        
    # action: accounts-list, setting: pattern
    # expects an array that looks like this:
    #   [ { u_id, username }, ... ]
    def list_accounts(self, pattern='%'):
        payload = self.__create_object('accounts-list', setting=pattern)
        response = self.__send_get(payload)
        users = []
        if response.status_code == requests.codes.ok:
            users = response.json()
        return [User(u['u_id'], u['username']) for u in users]
    
    # action: group-members-list, setting: groupname
    # expects an array that looks like this:
    #   [ { u_id, username }, ... ]
    def list_group_members(self, groupname):
        payload = self.__create_object('group-members-list', setting=groupname)
        response = self.__send_get(payload)
        users = []
        if response.status_code == requests.codes.ok:
            users = response.json()
        return [User(u['u_id'], u['username']) for u in users]
