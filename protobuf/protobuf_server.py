import time

import protobuf.service_pb2 as obj

from db import DBManager

def add_logging(fn):
    '''
    Higher-level function that wraps a function in order to log the function call.
    Prints out the function name, function arguments with which the function
    was called, and the return value.

    :param fn: function whose calls to wrap and log
    :return: the passed in function
    '''
    def fun(self, request, context):
        print '========================================================='
        print 'Servicing %s with arguments %s' % (fn.__name__, request)
        ret = fn(self, request, context)
        print 'Service returned %s' % ret
        print 'Done servicing %s' % fn.__name__
        return ret
    return fun

def list_to_protobuf(tpe):
    '''
    XXX CHECK THIS
    Higher-level function that converts a list of objects returns from the database
    to the corresponding protobuf objects to be sent to the client-protobuf layer.

    :param tpe: the protobuf object type to convert to
    :return: a function that wraps the return value of another function as the specified protobuf object type 
    '''
    def wrap(f):
        ''' 
        wraps the function that returns the list of values to be converted to protobuf object types

        :param f: the function whose return value is to be converted to a protobuf object type
        :return: the wrapping function
        '''
        def wrapped(self, request, context, *args, **kwargs):
            '''
            the wrapped function itself, which logs the function call and
            casts the return value to the specified type
            '''
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
    ''' 
    Runs the protobuf server with the ProtobufServer object that implements the
    server-side code for the client application rpc calls.

    The server listens to requests from the client on the specified port, and communicates with
    the database to retrieve and store client information.

    The server can be stopped by sending a keyboard interrupt, else the server will continue
    to run forever.

    :param port: the port on which the server listens for client requests 
    :return: does not return
    '''
    server = obj.beta_create_ChatApp_server(ProtobufServer())
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(1)

class ProtobufServer(obj.BetaChatAppServicer):
    ''' 
    ProtobufServer wraps the autogenerated protobuf code for server-side functions.

    This server implements the handling of the rpc functions specified in service.proto.
    Each function is passed a request argument, which is a protobuf message object 
    (e.g. a CMessage or User) defined in service.proto.

    The server communicates with the database and returns a protobuf message object 
    or list of these objects (e.g. Response, Group, User) so that the protobuf client
    wrapper can understand the server's response.
    '''
    def __init__(self):
        '''
        Initializes the protobuf server by setting up a database
        manager object for the server to communicate with.
        
        :return: ProtobufServer object
        '''
        self.db = DBManager()

    @add_logging
    def rpc_send_message(self, request, context):
        '''
        Sends the specified message in the message object to the specified user
        in the message object by inserting this message into the user table in the
        database.

        :param request: CMessage protobuf object.
        :return: protobuf Response object 
        '''
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
        '''
        Retrieves all the messages stored in the messages database table under this
        user's name.

        :param request: User protobuf object.
        :return: protobuf Message object stream on success, or empty list on error
        '''
        try:
            msgs = self.db.get_messages(request.u_id, request.checkpoint)
        except Exception as e:
            return []
        return msgs

    @add_logging
    def rpc_create_conversation(self, request, context):
        '''
        Creates a new conversation between two users by inserting
        a new "virtual group" into the database, and returns
        the group object corresponding to the new conversation.

        :param request: UserPair protobuf object.
        :return: Group protobuf object on success or error string
        '''
        try:
            u1 = self.db.get_user_id(request.username1)
            u2 = self.db.get_user_id(request.username2)
            gid = self.db.get_or_create_vgid(u1, u2)
            return obj.Group(g_id=gid)
        except Exception as e:
            return obj.Response(errno=1, msg=str(e))

    @add_logging
    def rpc_create_group(self, request, context):
        '''
        Creates a new group with 0 members by creating a new
        group into the database. The group must have a unique
        identifier, or else an error is returned

        :param request: Group protobuf object.
        :return: Group protobuf object on success, empty Group (with no name) on error
        '''
        g_name = request.g_name
        try:
            self.db.create_group(g_name)
            g_id = self.db.get_group_id(g_name)
        except Exception as e:
            return obj.Group(g_id=0, g_name="") 
        return obj.Group(g_id=g_id, g_name=g_name)

    @add_logging
    def rpc_create_account(self, request, context):
        '''
        Creates a new user account. The user must have a unique
        identifier, or else an error is returned.

        :param request: User protobuf object.
        :return: User protobuf object on success, empty User (with no name) on error
        '''
        username = request.username
        try:
            self.db.create_account(username)
            u_id = self.db.get_user_id(username)
        except Exception as e:
            return obj.User(u_id=0, username="") 
        return obj.User(u_id=u_id, username=username) 

    @add_logging
    def rpc_remove_account(self, request, context):
        '''
        Removes the account corresponding to the specified user.

        :param request: User protobuf object.
        :return: protobuf Response object indicating success or error
        '''
        try:
            self.db.remove_account(request.username)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_edit_group_name(self, request, context):
        '''
        Modify the group name of the specified group. 

        :param request: Group protobuf object.
        :return: protobuf Response object indicating success or error
        '''
        try:
            self.db.edit_group_name(request.g_name, request.new_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_remove_group_member(self, request, context):
        '''
        Remove a member from the specified group. 

        :param request: Group protobuf object (with "edit_member_name" field specified)
        :return: protobuf Response object indicating success or error
        '''
        try:
            self.db.remove_group_member(request.g_name, request.edit_member_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    def rpc_add_group_member(self, request, context):
        '''
        Add a member from the specified group. 

        :param request: Group protobuf object (with "edit_member_name" field specified)
        :return: protobuf Response object indicating success or error
        '''
        try:
            self.db.add_group_member(request.g_name, request.edit_member_name)
        except Exception as e:
            return obj.Response(errno=1, msg=e)
        return obj.Response(errno=0, msg="success!\n")

    @add_logging
    @list_to_protobuf(obj.User)
    def rpc_list_group_members(self, request, context):
        '''
        List members in the specified group. 

        :param request: Group protobuf object (with "edit_member_name" field specified)
        :return: stream of protobuf User objects (NULL User returned if error)
        '''
        try:
            users = self.db.get_group_members(request.g_name)
        except Exception as e:
            return [{'username': 'NULL'}]
        return users

    @add_logging
    @list_to_protobuf(obj.Group)
    def rpc_list_groups(self, request, context):
        '''
        List groups matching the specified pattern 

        :param request: Pattern protobuf object 
        :return: stream of protobuf Group objects (NULL Group returned if error)
        '''
        try:
            groups = self.db.get_groups(request.pattern)
        except Exception as e:
            return [{'g_id' : 0, 'g_name': 'NULL'}]
        return groups
        
    @add_logging
    @list_to_protobuf(obj.User)
    def rpc_list_accounts(self, request, context):
        '''
        List users matching the specified pattern 

        :param request: Pattern protobuf object 
        :return: stream of protobuf User objects (NULL User returned if error)
        '''
        try:
            users = self.db.get_accounts(request.pattern)
        except Exception as e:
            return [{'username': 'NULL'}]
        return users
