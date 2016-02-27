'''
This class implements the interface defined in protocols.py
and wraps the autogenerated protobuf code
'''

from grpc.beta import implementations
import protobuf.service_pb2 as obj

from protocols import Protocol, Message, User, Group

_TIMEOUT_SECONDS = 30

class Protobuf_Protocol(Protocol):

    def __get_response(self, response):
        if response.errno:
            return "Error: %s" % response.msg
        else: 
            return None

    # RUN
    def __init__(self, port):
        self.Channel = implementations.insecure_channel('localhost', port)
        self.Stub = obj.beta_create_ChatApp_stub(self.Channel)

    # MESSAGING 
    def send_message(self, from_name, dest_id, msg):
        message = obj.CMessage(
            to_id = dest_id,
            from_name = from_name,
            msg = msg
        )
        return self.__get_response(self.Stub.rpc_send_message(message, _TIMEOUT_SECONDS))

    def fetch_messages(self, to_id, checkpoint=0):
        user = obj.User(
            u_id = to_id,
            checkpoint = checkpoint
        )
        messages = self.Stub.rpc_get_messages(user, _TIMEOUT_SECONDS)
        return [Message(m.m_id, m.from_name, m.to_id, m.msg) for m in messages]

    def create_conversation(self, username1, username2):
        user_pair = obj.UserPair(
            username1=username1,
            username2=username2
        )
        group = self.Stub.rpc_create_conversation(user_pair, _TIMEOUT_SECONDS)
        return group.g_id

    # CREATION AND DELETION 
    def create_group(self, groupname):
        group = obj.Group(g_name = groupname)
        new_group = self.Stub.rpc_create_group(group, _TIMEOUT_SECONDS)
        if new_group.g_id != 0:
            return Group(new_group.g_id, new_group.g_name)
        else:
            return None
    def create_account(self, username):
        user = obj.User(username=username)
        new_user = self.Stub.rpc_create_account(user, _TIMEOUT_SECONDS)
        if new_user.u_id != 0:
            return User(new_user.u_id, new_user.username)
        else:
            return None
    def remove_account(self):
        user = obj.User(username=username)
        return self.__get_response(self.Stub.rpc_remove_account(user, _TIMEOUT_SECONDS))

    # GROUPS 
    def edit_group_name(self, old_name, new_name):
        group = obj.Group(g_name=old_name, new_name=new_name)
        return self.__get_response(self.Stub.rpc_edit_group_name(group, _TIMEOUT_SECONDS))
    def remove_group_member(self, groupname, member):
        group = obj.Group(g_name=groupname, edit_member_name=member)
        return self.__get_response(self.Stub.rpc_remove_group_member(group, _TIMEOUT_SECONDS))
    def add_group_member(self, groupname, member):
        group = obj.Group(g_name=groupname, edit_member_name=member)
        return self.__get_response(self.Stub.rpc_add_group_member(group, _TIMEOUT_SECONDS))

    # LISTING 
    def list_groups(self, pattern="%"):
        pattern = obj.Pattern(pattern=pattern) 
        groups = self.Stub.rpc_list_groups(pattern, _TIMEOUT_SECONDS)
        return [Group(g.g_id, g.g_name) for g in groups]
    def list_accounts(self, pattern="%"):
        pattern = obj.Pattern(pattern=pattern) 
        users = self.Stub.rpc_list_accounts(pattern, _TIMEOUT_SECONDS)
        return [User(u.u_id, u.username) for u in users]
    def list_group_members(self, groupname):
        group = obj.Group(
            g_name=groupname
        )
        users = self.Stub.rpc_list_group_members(group, _TIMEOUT_SECONDS)
        return [User(u.u_id, u.username) for u in users]
