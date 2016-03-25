'''
This file contains all functions necessary for the server to interface with the database!
'''

import sqlite3
import sys

def thread_safe(fn):
    '''Wraps db functions to be thread-safe.
    Every function invocation, it starts a new connection that it closes at the end.
    For an internal function taking arguments (connection, cursor, args),
    the wrapped function takes arguments (args).
    '''
    def new_fn(self, *args, **kwargs):
        conn = sqlite3.connect('chatapp.db')
        c = conn.cursor()
        try:
            ret = fn(self, conn, c, *args, **kwargs)
            conn.close()
            return ret
        except Exception as e:
	    conn.close()
            print 'Exception occured handling request %s: %s' % (fn.__name__, e)
	    raise e
    return new_fn

class DBManager(object):
    '''
    DBManager is the interface for the database layer of the application.
    To use, create a DBManager instance, and call one of the instance methods.
    Note that although instance methods appears to take conn and c as arguments,
    because of the decorator, we don't need to pass these arguments in
    '''
    def __init__(self):
        pass

    @thread_safe
    def create_tables(self, conn, c):
        '''
        create_tables(self): creates database tables for the app

        Returns None on success, raises an exception otherwise
        :return: None on success, raise an exception on error
        '''
        c.execute("""
            CREATE TABLE users (u_id int NOT NULL PRIMARY KEY, username varchar(255) UNIQUE)
        """)
        c.execute("""
            CREATE TABLE groups (g_id int NOT NULL PRIMARY KEY, g_name varchar(255) UNIQUE)
        """)
        c.execute("""
            CREATE TABLE vgroups (g_id int NOT NULL PRIMARY KEY, id1 int, id2 int)
        """)
        c.execute("""
            CREATE TABLE user_group_pairs (_id int NOT NULL PRIMARY KEY, u_id int, g_id int)
        """)
        c.execute("""
            CREATE TABLE messages (m_id int NOT NULL PRIMARY KEY, to_id int, from_id int, msg varchar(1023))
        """)
        conn.commit()

    @thread_safe
    def remove_tables(self, conn, c):
        '''
        create_tables(self): creates database tables for the app

        :return: None on success, raise an exception on error
        '''
        c.execute("""
            DROP TABLE users
        """)
        c.execute("""
            DROP TABLE groups
        """)
        c.execute("""
            DROP TABLE vgroups
        """)
        c.execute("""
            DROP TABLE user_group_pairs
        """)
        c.execute("""
            DROP TABLE messages
        """)
        conn.commit()

    @thread_safe
    def get_or_create_vgid(self, conn, c, to_id, from_id):
        '''
        get_or_create_vgid: given to_id and from_id (both user ids), finds a virtual group
        for these two users if it exists, or creates it if it does not.

        :param to_id: integer; user id of user you're sending message to
        :param from_id: integer; user id of user you're sending message from
        :return: integer; the id of the created vgroup on success, raises on error.
        '''
        c.execute("SELECT g_id FROM vgroups WHERE (id1 = ? AND id2 = ?) OR (id2 = ? AND id1 = ?)",
                      [to_id, from_id, to_id, from_id])
        v = c.fetchone()
        if v is None:
            c.execute("SELECT g_id FROM vgroups ORDER BY g_id DESC LIMIT 1")
            v = c.fetchone()
            if v is None:
                v = 0
            else:
                v = v[0]
            c.execute("INSERT INTO vgroups (g_id, id1, id2) VALUES (?, ?, ?)", [v + 2, to_id, from_id])
            self._insert_ugpair(conn, c, to_id, v+2)
            self._insert_ugpair(conn, c, from_id, v+2)
            to_id = v + 2
            conn.commit()
        else:
            to_id = v[0]

        return to_id

    @thread_safe
    def insert_message(self, conn, c, to_id, from_id, msg):
        '''
        insert_message: creates a new message from from_id to to_id with content msg.
            from_id is the id of a user.
            to_id is the id of a group or vgroup.

        :param to_id: integer; id of group or vgroup
        :param from_id: integer; id of the user sending message
        :return: None on success, raises on error
        '''
        if len(msg) > 1023:
            raise Exception('Message string too long')

        c.execute("""
            SELECT m_id FROM messages ORDER BY m_id DESC LIMIT 1
        """)
        v = c.fetchone()
        if v is None:
            v = 0
        else:
            v = v[0]
        c.execute("""
            INSERT INTO messages 
                       (m_id, to_id, from_id, msg)
                       VALUES
                       (?, ?, ?, ?)
                       """, [v + 1, to_id, from_id, msg])
        conn.commit()

    @thread_safe
    def get_user_id(self, conn, c, u_name):
        '''
        get_user_id: returns user id for user with given username

        :param u_name: string; username of user
        :return: integer; user id of user, raises on error (or if user doesn't exist)
        '''
        c.execute("SELECT u_id FROM users WHERE username=?", [u_name])
        v = c.fetchone()
        if v is None:
            raise Exception('User does not exist')

        return v[0]

    @thread_safe
    def get_group_id(self, conn, c, g_name):
        '''
        get_group_id: returns group id for group with given name

        :param g_name: string; name of the group
        :return integer representing id of group, raises on error (or if user doesn't exist)
        '''
        c.execute("SELECT g_id FROM groups WHERE g_name=?", [g_name])
        v = c.fetchone()
        if v is None:
            raise Exception('Group does not exist')

        return v[0]

    @thread_safe
    def get_messages(self, conn, c, u_id, checkpoint=0):
        '''
        get_messages: returns messages that specified user could see
        (messages addressed to that user or to a group the user belongs to),
        with message id greater than a specified checkpoint.

        :param u_id: integer; id of user
        :param checkpoint: integer; represents last received message id. Default 0.
        :return: a list of dictionaries representing messages (fields m_id, to_id, from_name, msg)
            on success, raises on error
        '''
        c.execute("""
            SELECT messages.m_id, messages.to_id, messages.from_id, messages.msg
                FROM messages INNER JOIN user_group_pairs ON
                    messages.to_id=user_group_pairs.g_id
                WHERE user_group_pairs.u_id=? AND messages.m_id>?
                ORDER BY messages.m_id ASC
            """, [u_id, checkpoint])
        rows = c.fetchall()
        if rows is None:
            raise Exception('No messages')
        answers = []
        for row in rows:
            c.execute("SELECT username FROM users WHERE u_id=?", [row[2]])
            user = c.fetchone()
            if user is None:
                raise Exception('From user does not exist')
            from_name = user[0]
            answers.append({'m_id': row[0], 'to_id': row[1], 'from_name': from_name, 'msg': row[3]})
        return answers

    @thread_safe
    def create_group(self, conn, c, g_name):
        '''
        create_group: creates a group with name g_name

        :param g_name: string; name of group to be created
        :return: None on success, raises on error
        '''
        c.execute("SELECT g_id FROM groups ORDER BY g_id DESC LIMIT 1")
        v = c.fetchone()
        if v is None:
            v = 1
        else:
            v = v[0]
        assert (v % 2 == 1)
        c.execute("""
            INSERT INTO groups 
                       (g_id, g_name)
                       VALUES
                       (?, ?)
                       """, [v + 2, g_name])
        conn.commit()

    def _insert_ugpair(self, conn, c, u_id, g_id):
        # helper function for associating user with id u_id with group with id g_id
        c.execute("SELECT _id FROM user_group_pairs ORDER BY _id DESC LIMIT 1")
        npairs = c.fetchone()
        if npairs is None:
            npairs = 0
        else:
            npairs = npairs[0]
        c.execute("""
            INSERT INTO user_group_pairs
                       (_id, u_id, g_id)
                       VALUES
                       (?, ?, ?)
                       """, [npairs + 1, u_id, g_id])

    @thread_safe
    def create_account(self, conn, c, u_name):
        '''
        create_account: creates a new user with username u_name

        :param u_name: string; name of new user
        :return: None on success, raises on error
        '''
        c.execute("SELECT u_id FROM users ORDER BY u_id DESC LIMIT 1")
        v = c.fetchone()
        if v is None:
            v = 0
        else:
            v = v[0]
        assert (v % 2 == 0)
        c.execute("""
            INSERT INTO users 
                       (u_id, username)
                       VALUES
                       (?, ?)
                       """, [v + 2, u_name])

        conn.commit()

    @thread_safe
    def add_group_member(self, conn, c, g_name, u_name):
        '''
        add_group_member: adds user with username u_name to group with name g_name

        :param g_name: string; name of group
        :param u_name: string; name of user to add to group
        :return: None on success, raises on error
        '''
        c.execute("SELECT u_id FROM users WHERE username=?", [u_name])
        u_id = c.fetchone()
        if u_id is None:
            raise Exception('User does not exist')
        else:
            u_id = u_id[0]

        c.execute("SELECT g_id FROM groups WHERE g_name=?", [g_name])
        g_id = c.fetchone()
        if g_id is None:
            raise Exception('Group does not exist')
        else:
            g_id = g_id[0]

        c.execute("SELECT _id FROM user_group_pairs WHERE u_id=? AND g_id=?",
                       [u_id, g_id])
        v = c.fetchone()
        if v is not None and len(v) > 0:
            raise Exception('User already in group')

        self._insert_ugpair(conn, c, u_id, g_id)
        conn.commit()


    @thread_safe
    def remove_account(self, conn, c, u_name):
        '''
        remove_account: Delete user with username u_name

        :param u_name: string; name of user to delete
        :return: None on success, raises on error
        '''
        c.execute("SELECT u_id FROM users WHERE username=?", [u_name])
        v = c.fetchone()
        if v is None:
            raise Exception("Deleted user doesn't exit")
        else:
            v = v[0]

        c.execute("DELETE FROM users WHERE u_id=?", [v])
        c.execute("DELETE FROM user_group_pairs WHERE u_id=?", [v])
        conn.commit()

    @thread_safe
    def remove_group_member(self, conn, c, g_name, u_name):
        '''
        remove_group_member: Delete user with username u_name from group with name g_name

        :param g_name: string; name of group
        :param u_name: string; name of user to remove from group
        :return: None on success, raises on error
        '''
        c.execute("SELECT u_id FROM users WHERE username=?", [u_name])
        uid = c.fetchone()
        if uid is None:
            raise Exception("User doesn't exist")
        else:
            uid = uid[0]

        c.execute("SELECT g_id FROM groups WHERE g_name=?", [g_name])
        gid = c.fetchone()
        if gid is None:
            raise Exception("Group doesn't exist")
        else:
            gid = gid[0]

        c.execute("DELETE FROM user_group_pairs WHERE u_id=? AND g_id=?", [uid, gid])
        conn.commit()

    @thread_safe
    def edit_group_name(self, conn, c, g_name, newname):
        '''
        edit_group_name: change name of group with name g_name to newname

        :param g_name: string; the old name of the group
        :param newname: string; the new name of the group
        :return: None on success, raises on error
        '''
        c.execute("UPDATE groups SET g_name=? WHERE g_name=?", [newname, g_name])
        conn.commit()

    @thread_safe
    def get_groups(self, conn, c, pattern):
        '''
        get_groups: returns a list of groups whose names matches pattern.
            pattern is specified in SQL pattern syntax.

        :param pattern: string; pattern to match, specified in SQL pattern syntax
        :return: list of dictionaries representing groups (fields: group id, group name)
        '''
        c.execute("SELECT g_id, g_name FROM groups WHERE g_name LIKE ?", [pattern])
        groups = c.fetchall()
        if groups is None:
            return []
        return [{'g_id': g[0], 'g_name': g[1]} for g in groups]

    @thread_safe
    def get_accounts(self, conn, c, pattern):
        '''
        get_accounts: returns a list of users whose usernames matches pattern.
            pattern is specified in SQL pattern syntax.

        :param pattern: string; pattern to match, specified in SQL pattern syntax
        :return: list of dictionaries representing users (fields: user id, username)
        '''
        c.execute("SELECT u_id, username FROM users WHERE username LIKE ? ORDER BY u_id ASC", [pattern])
        users = c.fetchall()
        if users is None:
            return []
        return [{'u_id': u[0], 'username': u[1]} for u in users]

    @thread_safe
    def get_group_members(self, conn, c, g_name):
        '''
        get_group_members: returns a list of users belong to group with name g_name

        :param g_name: string; name of group
        :return: list of dictionaries representing users belonging to group
            (fields: user id, username)
        '''
        c.execute("""
            SELECT users.u_id, users.username FROM
                users INNER JOIN user_group_pairs ON users.u_id=user_group_pairs.u_id
                INNER JOIN groups ON user_group_pairs.g_id=groups.g_id
                WHERE groups.g_name=?""", [g_name])
        users = c.fetchall()
        if users is None:
            return []
        return [{'u_id': u[0], 'username': u[1]} for u in users]

def test(db):
    '''
    Given a clean database (no tables), tests all our database functionality.
    '''
    db.create_tables()
    db.create_account("fding")
    db.create_account("tslilyai")
    db.create_account("pafnuty.chebyshev")
    db.create_account("agrothendieck")
    db.create_account("ludwig")
    db.create_account("johann")
    db.create_account("wolfgang")
    try:
        db.create_account("johann")
        raise Exception('DB Allowed creation of duplicate')
    except Exception as e:
        print 'Caught expected exception %s' % e


    db.create_group("composers")
    db.create_group("mathematicians")
    db.create_group("students")
    db.create_group("dead.people")

    db.add_group_member("composers", "ludwig")
    db.add_group_member("composers", "johann")
    db.add_group_member("composers", "wolfgang")
    db.add_group_member("mathematicians", "pafnuty.chebyshev")
    db.add_group_member("mathematicians", "agrothendieck")
    db.add_group_member("students", "fding")
    db.add_group_member("students", "tslilyai")
    try:
        db.add_group_member("tslilyai", "students")
        raise Exception('DB Allowed creation of duplicate')
    except Exception as e:
        print 'Caught expected exception %s' % e

    db.add_group_member("dead.people", "ludwig")
    db.add_group_member("dead.people", "johann")
    db.add_group_member("dead.people", "wolfgang")
    db.add_group_member("dead.people", "pafnuty.chebyshev")
    db.add_group_member("dead.people", "agrothendieck")

    res = db.get_groups("%s")
    assert tuple([r['g_name'] for r in res]) == ('composers', 'mathematicians', 'students')

    res = db.get_accounts("______")
    assert tuple([r['username'] for r in res]) == ('ludwig', 'johann')

    res = db.get_group_members("composers")
    assert tuple([r['username'] for r in res]) == ('ludwig', 'johann', 'wolfgang')


    vgid = db.get_or_create_vgid(db.get_user_id("tslilyai"), db.get_user_id("fding"))
    db.insert_message(vgid,
                      db.get_user_id("fding"),
                      "Hi!")

    db.insert_message(db.get_group_id("students"),
                      db.get_user_id("fding"),
                      "lets pset")

    db.insert_message(db.get_group_id("mathematicians"),
                      db.get_user_id("fding"),
                      "Teach me algebraic geometry")

    db.insert_message(db.get_group_id("dead.people"),
                      db.get_user_id("tslilyai"),
                      "What is heaven like?")

    db.insert_message(db.get_group_id("composers"),
                      db.get_user_id("agrothendieck"),
                      "your music reminded me of quasicoherent sheaves of ideals")

    def get_contents(ls):
        return tuple([l['msg'] for l in ls])
    # Time to check the messages
    msgs = db.get_messages(db.get_user_id("fding"))
    assert get_contents(msgs) == ('Hi!', 'lets pset',)

    msgs = db.get_messages(db.get_user_id("tslilyai"))
    assert get_contents(msgs) == ('Hi!', 'lets pset')
    
    
    msgs = db.get_messages(db.get_user_id("pafnuty.chebyshev"))
    assert get_contents(msgs) == ('Teach me algebraic geometry', 'What is heaven like?')
    msgs = db.get_messages(db.get_user_id("agrothendieck"))
    assert get_contents(msgs) == ('Teach me algebraic geometry', 'What is heaven like?')
    msgs = db.get_messages(db.get_user_id("ludwig"))
    assert get_contents(msgs) == ('What is heaven like?', 'your music reminded me of quasicoherent sheaves of ideals')
    msgs = db.get_messages(db.get_user_id("johann"))
    assert get_contents(msgs) == ('What is heaven like?', 'your music reminded me of quasicoherent sheaves of ideals')
    msgs = db.get_messages(db.get_user_id("wolfgang"))
    assert get_contents(msgs) == ('What is heaven like?', 'your music reminded me of quasicoherent sheaves of ideals')


    db.edit_group_name('students', 'STUDENTS')
    db.get_group_id('STUDENTS')
    try:
        db.get_group_id("students")
        raise Exception('DB rename failed')
    except Exception as e:
        print 'Caught expected exception %s' % e

    msgs = db.get_messages(db.get_user_id("fding"))
    assert get_contents(msgs) == ('Hi!', 'lets pset',)

    msgs = db.get_messages(db.get_user_id("tslilyai"))
    assert get_contents(msgs) == ('Hi!', 'lets pset')

    print 'Passed all tests'

if __name__ == '__main__':
    db = DBManager()

    if len(sys.argv) == 2:
        if sys.argv[1] == 'init':
            db.create_tables()
        elif sys.argv[1] == 'clean':
            db.remove_tables()
            db.create_tables()
        elif sys.argv[1] == 'test':
            db.remove_tables()
            test(db)
        else:
            print 'Usage: db init|clean|test'
    else:
        db.create_tables()

    
