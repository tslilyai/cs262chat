''' 
This wraps the autogenerated protobuf code for server-side functions
'''
import time

import protobuf.service_pb2 as obj

from db import DBManager

def add_logging(fn):
    def fun(self, request, context):
        print '========================================================='
        print 'Servicing %s with arguments %s' % (fn.__name__, request)
        ret = fn(self, request, context)
        print 'Service returned %s' % ret
        print 'Done servicing %s' % fn.__name__
        return ret
    return fun

def list_to_protobuf(tpe):
    def wrap(f):
        def wrapped(self, request, context, *args, **kwargs):
            print 'Running %s with arguments %s' % (f.__name__, request)
            ret = f(self, request, context, *args, **kwargs)
            assert isinstance(ret, list)
            for r in ret:
                print "Yielding service returned ", str(r)
                print tpe
                print 'Tpe %s' % tpe(**r)
                yield tpe(**r)
        wrapped.__name__ = f.__name__
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
    def rpc_send_message(self, request, context):
        try:
            to_id = request.to_id
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
            msgs = self.db.get_messages(request.u_id, request.checkpoint)
        except Exception as e:
            # return a dummy message if getting messages failed
            return []
        # {'m_id': 0, 'to_name': 'NULL', 'from_name': 'NULL', 'msg': 'Could not retrieve messages :%s\n' % e}]
        return msgs

    @add_logging
    def rpc_create_conversation(self, request, context):
        try:
            u1 = self.db.get_user_id(request.username1)
            u2 = self.db.get_user_id(request.username2)
            gid = self.db.get_or_create_vgid(u1, u2)
            return obj.Group(g_id=gid)
        except Exception as e:
            return obj.Response(errno=1, msg=str(e))

    @add_logging
    def rpc_create_group(self, request, context):
        g_name = request.g_name
        try:
            self.db.create_group(g_name)
            g_id = self.db.get_group_id(g_name)
        except Exception as e:
            return obj.Group(g_id=0, g_name="") 
        return obj.Group(g_id=g_id, g_name=g_name)

    @add_logging
    def rpc_create_account(self, request, context):
        username = request.username
        try:
            self.db.create_account(username)
            u_id = self.db.get_user_id(username)
        except Exception as e:
            print "user not created: %s" % e
            return obj.User(u_id=0, username="") 
        return obj.User(u_id=u_id, username=username) 

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
            self.db.add_group_member(request.g_name, request.edit_member_name)
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
            return [{'g_id' : 0, 'g_name': 'NULL'}]
        return groups
        
    @add_logging
    @list_to_protobuf(obj.User)
    def rpc_list_accounts(self, request, context):
        try:
            users = self.db.get_accounts(request.pattern)
        except Exception as e:
            return [{'username': 'NULL'}]
        return users
