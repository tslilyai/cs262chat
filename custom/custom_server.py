''' 
This is the code for server-side functions for the
custom wire protocol
'''

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from db import DBManager
import cgi
import urlparse
import json

# decorators to standardize logging and return-by-HTTP

def add_logging(fn):
    def fun(self, payload):
        print '========================================================='
        print 'Servicing %s with arguments %s' % (fn.__name__, payload)
        ret = fn(self, payload)
        if ret is None:
            print 'Service failed'
        else:
            print 'Service returned %s' % ret
        print 'Done servicing %s' % fn.__name__
        return ret
    return fun

'''
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
'''

class CustomHTTPServer(HTTPServer):
    def set_db(self, db):
        self.db = db

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        # creates a payload that looks like { 'arg0': ['value'], ... }
        origPayload = urlparse.parse_qs(parsed_path.query)
        parsedPayload = {}
        for key in origPayload.keys():
            parsedPayload[key] = origPayload[key][0]
        
        print(parsed_path.query)
        print(parsedPayload)
        
        # switch on parsedPayload['action'], send to helper functions
        actionFuncMapping = {
            'messages-fetch': self.__messages_fetch,
            'groups-list': self.__groups_list,
            'accounts-list': self.__accounts_list,
            'group-members-list': self.__group_members_list
        }
        
        func = actionFuncMapping[parsedPayload['action']]
        response = func(parsedPayload)
        
        if response != None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response))
        else:
            self.send_response(500)
            self.end_headers()
            
        return # CustomRequestHandler sends self.current_response automatically
    
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        payload = json.loads(self.rfile.read(length))
        
        # switch on payload['action'], send to helper functions
        actionFuncMapping = {
            'message-send': self.__message_send,
            'conversation-create': self.__conversation_create,
            'group-create': self.__group_create,
            'account-create': self.__account_create,
            'account-remove': self.__account_remove,
            'group-name-edit': self.__group_name_edit,
            'group-member-remove': self.__group_member_remove,
            'group-member-add': self.__group_member_add
        }
        
        func = actionFuncMapping[payload['action']]
        response = func(payload)
        
        if response != None:
            self.send_response(200)
            self.end_headers()
            if '200_no_response' not in response:
                self.wfile.write(json.dumps(response))
        else:
            self.send_response(500)
            self.end_headers()
        
        return
    
    # functions to actually do things:
    '''
    def __message_send(self, payload):
        raise NotImplementedError
        
    def __messages_fetch(self, payload):
        raise NotImplementedError
    
    def __conversation_create(self, payload):
        raise NotImplementedError
    
    def __group_create(self, payload):
        raise NotImplementedError
    
    def __account_create(self, payload):
        raise NotImplementedError
    
    def __account_remove(self, payload):
        raise NotImplementedError
        
    def __group_name_edit(self, payload):
        raise NotImplementedError
    
    def __group_member_remove(self, payload):
        raise NotImplementedError
    
    def __group_member_add(self, payload):
        raise NotImplementedError
    
    def __groups_list(self, payload):
        raise NotImplementedError
    
    def __accounts_list(self, payload):
        raise NotImplementedError
    
    def __group_members_list(self, payload):
        raise NotImplementedError
    '''
##############################################################################

    @add_logging
    def __message_send(self, payload):
        try:
            to_id = payload['target']
            from_id = self.server.db.get_user_id(payload['actor'])
            msg = payload['value']
            self.server.db.insert_message(to_id, from_id, msg)
        except Exception as e:
            return None 
        return { '200_no_response': 1 }
    
    @add_logging
    #@list_to_protobuf(obj.CMessage)
    def __messages_fetch(self, payload):
        try:
            msgs = self.server.db.get_messages(payload['actor'], payload['setting'])
        except Exception as e:
            print str(e)
            return None
        return msgs

    @add_logging
    def __conversation_create(self, payload):
        try:
            u1 = self.server.db.get_user_id(payload['actor'])
            u2 = self.server.db.get_user_id(payload['target'])
            g_id = self.server.db.get_or_create_vgid(u1, u2)
        except Exception as e:
            return None
        return {'g_id':g_id}

    @add_logging
    def __group_create(self, payload):
        g_name = payload['value']
        try:
            self.server.db.create_group(g_name)
            g_id = self.server.db.get_group_id(g_name)
        except Exception as e:
            return None
        return {'g_name':g_name, 'g_id':g_id}

    @add_logging
    def __account_create(self, payload):
        username = payload['value']
        try:
            self.server.db.create_account(username)
            u_id = self.server.db.get_user_id(username)
        except Exception as e:
            print "user not created: %s" % e
            return None
        return {'username':username, 'u_id':u_id}

    @add_logging
    def __account_remove(self, payload):
        try:
            self.server.db.remove_account(payload['target'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_name_edit(self, payload):
        try:
            self.server.db.edit_group_name(payload['target'], payload['value'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_member_remove(self, payload):
        try:
            self.server.db.remove_group_member(payload['target'], payload['value'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_member_add(self, payload):
        try:
            self.server.db.add_group_member(payload['target'], payload['value'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    #@list_to_protobuf(obj.User)
    def __group_members_list(self, payload):
        try:
            users = self.server.db.get_group_members(payload['setting'])
        except Exception as e:
            return None
        return users

    @add_logging
    #@list_to_protobuf(obj.Group)
    def __groups_list(self, payload):
        try:
            groups = self.server.db.get_groups(payload['setting'])
        except Exception as e:
            return None
        return groups
        
    @add_logging
    #@list_to_protobuf(obj.User)
    def __accounts_list(self, payload):
        try:
            users = self.server.db.get_accounts(payload['setting'])
        except Exception as e:
            return None
        return users

##############################################################################

def run(port=8080):
    server_address = ('', port)
    server_class = CustomHTTPServer
    handler_class = CustomRequestHandler
    httpd = server_class(server_address, handler_class)
    httpd.set_db(DBManager())
    print 'Starting httpd...'
    httpd.serve_forever()
        
if __name__ == '__main__':
    run()