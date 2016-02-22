''' 
This wraps the autogenerated protobuf code for server-side functions
'''

import service_pb2 as obj
import db

class ProtobufServer(service_pb2.beta_create_ChatApp_server):
    def __init__(self):
        self.db = DBManager()

    def rpc_send_individual_message(self, request, context):
        try:
            to_id = self.db.get_user_id(request.to_name)
            from_id = self.db.get_user_id(request.from_name)
            msg = request.msg
            self.db.insert_message(to_id, from_id, msg)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")
    
    def rpc_send_group_message(self, request, context):
        try:
            to_id = self.db.get_group_id(request.to_name)
            from_id = self.db.get_user_id(request.from_name)
            msg = request.msg
            self.db.insert_message(to_id, from_id, msg)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_get_messages(self, request, context):
        try:
            u_id = self.db.get_user_id(request.username)
            msgs = self.db.get_messages(u_id)
        except Exception as e:
            # return a dummy message if getting messages failed
            yield obj.CMessage(
                    to_name="NULL",
                    from_name="NULL",
                    msg="Could not retrieve messages\n"
                )
        for msg in self.db.get_messages(u_id):
            yield msg

    def rpc_create_group(self, request, context):
        groupname = request.g_name
        try:
            self.db.create_group(groupname)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_create_account(self, request, context):
        username = request.username
        try:
            self.db.create_account(username)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_remove_account(self, request, context):
        try:
            self.db.remove_account(request.username)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_edit_group_name(self, request, context):
        try:
            self.db.edit_group_name(request.g_name, request.new_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_remove_group_member(self, request, context):
        try:
            self.db.remove_group_member(request.g_name, request.edit_member_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_add_group_member(self, request, context):
        try:
            self.db.add_move_member(request.g_name, request.edit_member_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    def rpc_list_group_members(self, request, context):
        try:
            users = self.db.get_group_members(request.g_name)
        except Exception as e:
            yield obj.User(username="NULL")
        for user in users:
            yield user

    def rpc_list_groups(self, request, context):
        try:
            groups = self.db.get_groups(request.pattern)
        except Exception as e:
            yield obj.Group(g_name="NULL")
        for group in groups:
            yield group
        
    def rpc_list_accounts(self, request, context):
        try:
            users = self.db.get_accounts(request.pattern)
        except Exception as e:
            yield obj.User(username="NULL")
        for user in users:
            yield user 
