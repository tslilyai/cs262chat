from custom_client import CustomProtocol as Proto

def u_user_create(client, username):
    print 'creating user '+username+'...'
    account = client.create_account(username)
    if account is None:
        print 'Error on <create_account>.'
        print 'stop.'
        exit(1)
    #else
    print 'created user '+account.username+' with id '+str(account.u_id)+'.'
    accounts = u_accounts_list(client)
    if username not in [u.username for u in accounts]:
        print 'Logical Error: user '+username+' not present after successful create.'
        print 'stop.'
        exit(1)
    #else
    print '(confirmed: user '+username+' is present)'

# removes a user
def u_user_remove(client,username):
    print 'removing user '+username+'...'
    response = client.remove_account(username)
    if response is None:
        print 'success.'
        return
    else:
        print 'on <remove_account>'
        print response
        exit(1)
    accounts = u_accounts_list(client)
    if username in [u.username for u in accounts]:
        print 'Logical Error: user '+username+' present after successful remove.'
        print 'stop.'
        exit(1)
    #else
    print '(confirmed: user '+username+' is not present)'
    

def u_accounts_list(client,check_if_empty=False):
    if not check_if_empty:
        print 'listing accounts...'
        accounts = client.list_accounts()
        print str(len(accounts))+' accounts found.'
        return accounts
    
    #else
    accounts = u_accounts_list(client)
    if len(accounts) == 0:
        print 'no accounts; is this an error?'
        print '(creating a test user to find out)'
        
        u_user_create(client,'utest0')
        accounts = u_accounts_list(client)
        if len(accounts) == 0:
            print 'Logical Error: no accounts, even after successful create.'
            print 'stop.'
            exit(1)
        #else
        print 'okay, "no accounts" was not an error.'
        
        u_user_remove(client,'utest0')
        accounts = u_accounts_list(client)
        if len(accounts) != 0:
            print 'Logical Error: accounts '+accounts[0]+' and '+str(len(accounts))+' others remain after successful remove.'
            print 'stop.'
            exit(1)
    print 'Success: <list_accounts> works. (found '+str(len(accounts))+' accounts)'

def u_group_create(client, g_name):
    print 'creating group '+g_name+'...'
    group = client.create_account(g_name)
    if group is None:
        print 'Error on <create_group>.'
        print 'stop.'
        exit(1)
    #else
    print 'created group '+group.g_name+' with id '+str(group.g_id)+'.'
    groups = u_groups_list(client)
    if g_name not in [g.g_name for g in groups]:
        print 'Logical Error: group '+g_name+' not present after successful create.'
        print 'stop.'
        exit(1)
    #else
    print '(confirmed: group '+g_name+' is present)'

# removes a user
def u_group_remove(client,g_name):
    print 'removing group '+g_name+'...'
    response = client.remove_group(g_name)
    if response is None:
        print 'success.'
        return
    else:
        print 'on <remove_group>'
        print response
        exit(1)
    groups = u_groups_list(client)
    if g_name in [g.g_name for g in groups]:
        print 'Logical Error: group '+g_name+' present after successful remove.'
        print 'stop.'
        exit(1)
    #else
    print '(confirmed: group '+g_name+' is not present)'
    

def u_groups_list(client,check_if_empty=False):
    if not check_if_empty:
        print 'listing groups...'
        groups = client.list_groups()
        print str(len(groups))+' groups found.'
        return groups
    
    #else
    groups = u_groups_list(client)
    if len(groups) == 0:
        print 'no groups; is this an error?'
        print '(creating a test group to find out)'
        
        u_group_create(client,'utestG0')
        groups = u_groups_list(client)
        if len(groups) == 0:
            print 'Logical Error: no groups, even after successful create.'
            print 'stop.'
            exit(1)
        #else
        print 'okay, "no groups" was not an error.'
        
        u_group_remove(client,'utestG0')
        groups = u_accounts_list(client)
        if len(groups) != 0:
            print 'Logical Error: groups '+groups[0]+' and '+str(len(groups))+' others remain after successful remove.'
            print 'stop.'
            exit(1)
    print 'Success: <list_groups> works. (found '+str(len(groups))+' groups)'

client = Proto()

