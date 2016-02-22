''' 
This wraps the autogenerated protobuf code for server-side functions
'''
import time
import protobuf.service_pb2 as obj
from db import DBManager
import types
import itertools

def add_logging(fn):
    def fun(self, request, context):
        print '========================================================='
        print 'Servicing %s with arguments %s' % (fn.__name__, request)
        ret = fn(self, request, context)
        pval = None
        if isinstance(ret, types.GeneratorType):
            pval = []
            ret, rbackup = itertools.tee(ret)
            for r in rbackup:
                print str(r)
                pval.append(r)
            pval = ', '.join(pval)
        else:
            pval = ret
        print 'Service returned %s' % pval
        print 'Done servicing %s' % fn.__name__
        return ret
    return fun

def list_to_protobuf(tpe):
    def wrap(f):
        def wrapped(*args, **kwargs):
            ret = f(*args, **kwargs)
            assert isinstance(ret, list):
            for r in ret:
                yield tpe(**r)
        return wrapped
    return wrap

def run(port):
    server = obj.beta_create_ChatApp_server(ProtobufServer())
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(1)

class ProtobufServer(obj.BetaChatAppServicer):
    def __init__(self):
        self.db = DBManager()

    @add_logging
    def rpc_send_individual_message(self, request, context):
        try:
            to_id = db.get_user_id(request.to_name)
            from_id = self.db.get_user_id(request.from_name)
            msg = request.msg
            self.db.insert_message(to_id, from_id, msg)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")
    
    @add_logging
    def rpc_send_group_message(self, request, context):
        try:
            to_id = self.db.get_group_id(request.to_name)
            from_id = self.db.get_user_id(request.from_name)
            msg = request.msg
            self.db.insert_message(to_id, from_id, msg)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    @list_to_protobuf(obj.CMessage)
    def rpc_get_messages(self, request, context):
        try:
            u_id = self.db.get_user_id(request.username)
            msgs = self.db.get_messages(u_id)
        except Exception as e:
            # return a dummy message if getting messages failed
            return [{'to_name': 'NULL', 'from_name': 'NULL', 'msg': 'Could not retrieve messages :%s\n' % e}]
        return self.db.get_messages(u_id)

    @add_logging
    def rpc_create_group(self, request, context):
        groupname = request.g_name
        try:
            self.db.create_group(groupname)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_create_account(self, request, context):
        username = request.username
        try:
            self.db.create_account(username)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_remove_account(self, request, context):
        try:
            self.db.remove_account(request.username)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_edit_group_name(self, request, context):
        try:
            self.db.edit_group_name(request.g_name, request.new_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_remove_group_member(self, request, context):
        try:
            self.db.remove_group_member(request.g_name, request.edit_member_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_add_group_member(self, request, context):
        try:
            self.db.add_move_member(request.g_name, request.edit_member_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    @list_to_protobuf(obj.User)
    def rpc_list_group_members(self, request, context):
        try:
            users = self.db.get_group_members(request.g_name)
        except Exception as e:
            return [{'username': 'NULL'}]
        return users

    @add_logging
    @list_to_protobuf(obj.Group)
    def rpc_list_groups(self, request, context):
        try:
            groups = self.db.get_groups(request.pattern)
        except Exception as e:
            return [{'g_name': 'NULL'}]
        return groups
        
    @add_logging
    @list_to_protobuf(obj.User)
    def rpc_list_accounts(self, request, context):
        try:
            users = self.db.get_accounts(request.pattern)
        except Exception as e:
            return [{'username': 'NULL'}]
        return users
