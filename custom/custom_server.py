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
    '''
    Higher-level function that wraps a function in order to log the function call.
    Prints out the function name, function arguments with which the function
    was called, and the return value.

    :param fn: function whose calls we want to log
        fn is assumed to take as an argument a payload
    :return: a new function that does logging before and after calling fn
    '''
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

class CustomHTTPServer(HTTPServer):
    '''
    CustomHTTPServer just inherits the functionality of HTTPServer to handler_class
    all the HTTP requests and such.  It takes in a DBManager, defined in db.py.

    The meat of all the requests is handled in CustomRequestHandler.
    '''
    def set_db(self, db):
        self.db = db

class CustomRequestHandler(BaseHTTPRequestHandler):
    '''
    CustomRequestHandler is the class that translates between HTTP requests and what
    should actually be done.  This class processes an HTTP request, does the requisite
    server action, and returns something to the client.

    The server communicates with the database and returns JSON-like objects - sometimes
    arrays, sometimes objects - depending on the specific function.
    '''
    def do_GET(self):
        '''
        The function that handles all GET requests.  This function is called whenever
        a GET request is made to the server.  It looks at the action, and calls another
        function based on the action, passing the rest of the request payload to the
        function.

        Since GET does not come with a payload, parameters are specified in the query
        string of the GET request.

        This path can be called by sending a GET request to /?val1=param1&val2=param2
        with the query string parameters.
        '''
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
        '''
        The function that handles all POST requests.  This function is called whenever
        a POST request is made to the server.  It looks at the action, and calls another
        function based on the action, passing the rest of the request payload to the
        function.

        The payload is expected to be a JSON object in the regular POST payload body.
        '''
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
    
##############################################################################
    '''
    The methods handle all the requests. Routing to each request is handled
    in do_GET and do_POST. Documentation describes what is expected in payload,
    what the method does, and what the method returns.
    '''

    @add_logging
    def __message_send(self, payload):
        '''
        action: message-send, actor: from_id, target: dest_id, value: msg
        Sends msg from from_id to dest_id
        returns nothing
        '''
        try:
            to_id = payload['target']
            from_id = self.server.db.get_user_id(payload['actor'])
            msg = payload['value']
            self.server.db.insert_message(to_id, from_id, msg)
        except Exception as e:
            return None 
        return { '200_no_response': 1 }
    
    @add_logging
    def __messages_fetch(self, payload):
        '''
        action: messages-fetch, actor: to_id, setting: checkpoint
        Fetches all messages sent to to_id, with checkpoint

        returns an array that looks like this:
            [ { m_id, from_name, to_id, msg }, ... ]
        '''
        try:
            msgs = self.server.db.get_messages(payload['actor'], payload['setting'])
        except Exception as e:
            print str(e)
            return None
        return msgs

    @add_logging
    def __conversation_create(self, payload):
        '''
        action: conversation-create, actor: username1, target: username2
        Create a conversation between username1 and username2
        returns a { g_id: g_id } object back, g_id = 0 means something went wrong
        '''
        try:
            u1 = self.server.db.get_user_id(payload['actor'])
            u2 = self.server.db.get_user_id(payload['target'])
            g_id = self.server.db.get_or_create_vgid(u1, u2)
        except Exception as e:
            return None
        return {'g_id':g_id}

    @add_logging
    def __group_create(self, payload):
        '''
        action: group-create, value: groupname
        Create a group with name groupname
        returns a { g_id: g_id, g_name: g_name } object back
        '''
        g_name = payload['value']
        try:
            self.server.db.create_group(g_name)
            g_id = self.server.db.get_group_id(g_name)
        except Exception as e:
            return None
        return {'g_name':g_name, 'g_id':g_id}

    @add_logging
    def __account_create(self, payload):
        '''
        action: account-create, value: username
        Create an account with name username
        returns a { username, u_id } object back
        '''
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
        '''
        action: account-remove, value: username
        returns nothing
        '''
        try:
            self.server.db.remove_account(payload['target'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_name_edit(self, payload):
        '''
        action: group-edit-name, target: old_name, value: new_name
        Change name of group with name old_name to new_name
        returns nothing
        '''
        try:
            self.server.db.edit_group_name(payload['target'], payload['value'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_member_remove(self, payload):
        '''
        action: group-edit-name, target: groupname, value: member
        removes member from groupname
        returns nothing
        '''
        try:
            self.server.db.remove_group_member(payload['target'], payload['value'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_member_add(self, payload):
        '''
        action: group-add-name, target: groupname, value: member
        adds member to groupname
        returns nothing
        '''
        try:
            self.server.db.add_group_member(payload['target'], payload['value'])
        except Exception as e:
            return None
        return { '200_no_response': 1 }

    @add_logging
    def __group_members_list(self, payload):
        '''
        action: group-members-list, setting: groupname
        list the members of groupname
        returns an array that looks like this:
            [ { u_id, username }, ... ]
        '''
        try:
            users = self.server.db.get_group_members(payload['setting'])
        except Exception as e:
            return None
        return users

    @add_logging
    def __groups_list(self, payload):
        '''
        action: groups-list, setting: pattern
        list all groups that match the pattern; pattern is a simple SQL
        returns an array that looks like this:
            [ { g_id, g_name }, ... ]
        '''
        try:
            groups = self.server.db.get_groups(payload['setting'])
        except Exception as e:
            return None
        return groups
        
    @add_logging
    def __accounts_list(self, payload):
        '''
        action: accounts-list, setting: pattern
        list accounts that match pattern, a simple SQL pattern
        returns an array that looks like this:
            [ { u_id, username }, ... ]
        '''
        try:
            users = self.server.db.get_accounts(payload['setting'])
        except Exception as e:
            return None
        return users

##############################################################################

def run(port=8080):
    '''
    Runs the custom server with the CustomHTTPServer and CustomRequestHandler that
    implements the server-side code for the client HTTP interface calls.

    The server listens to requests from the client on the specified port, and communicates with
    the database to retrieve and store client information.

    The server can be stopped by sending a keyboard interrupt, else the server will continue
    to run forever.

    :param port: the port on which the server listens for client requests 
    :return: does not return
    '''
    server_address = ('', port)
    server_class = CustomHTTPServer
    handler_class = CustomRequestHandler
    httpd = server_class(server_address, handler_class)
    httpd.set_db(DBManager())
    print 'Starting httpd...'
    httpd.serve_forever()
        
if __name__ == '__main__':
    '''
    Just a driver to run the server on port 8080
    '''
    run()