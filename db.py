'''
This file contains all functions necessary for the server to interface with the database!
'''

import sqlite3
import threading

def thread_safe(fn):
    def new_fn(*args, **kwargs):
        with args[0].lock:
            args[0].conn = sqlite3.connect('chatapp.db')
            args[0].c = args[0].conn.cursor()
            return fn(*args, **kwargs)
    return new_fn

class DBManager(object):
    def __init__(self):
        self.lock = threading.Lock()

    def __del__(self):
        self.conn.close()

    @thread_safe
    def create_tables(self):
        self.c.execute("""
            CREATE TABLE users (u_id int NOT NULL PRIMARY KEY, username varchar(255) UNIQUE)
        """)
        self.c.execute("""
            CREATE TABLE groups (g_id int NOT NULL PRIMARY KEY, gname varchar(255) UNIQUE)
        """)
        self.c.execute("""
            CREATE TABLE vgroups (g_id int NOT NULL PRIMARY KEY, id1 int, id2 int)
        """)
        self.c.execute("""
            CREATE TABLE user_group_pairs (_id int NOT NULL PRIMARY KEY, u_id int, g_id int)
        """)
        self.c.execute("""
            CREATE TABLE messages (m_id int NOT NULL PRIMARY KEY, to_id int, from_id int, msg varchar(1023))
        """)
        self.conn.commit()

    @thread_safe
    def insert_message(self, to_id, from_id, msg):
        if len(msg) > 1023:
            raise Exception('Message string too long')

        if to_id % 2 == 0:
            # User id. Look up vgroup
            self.c.execute("SELECT g_id FROM vgroups WHERE (id1 = ? AND id2 = ?) OR (id2 = ? AND id1 = ?)",
                          [to_id, from_id, from_id, to_id])
            v = self.c.fetchone()
            if v is None:
                self.c.execute("SELECT g_id FROM vgroups ORDER BY g_id DESC LIMIT 1")
                v = self.c.fetchone()
                if v is None:
                    v = 0
                else:
                    v = v[0]
                self.c.execute("INSERT INTO vgroups (g_id, id1, id2) VALUES (?, ?, ?)", [v + 2, to_id, from_id])
                self._insert_ugpair(to_id, v+2)
                self._insert_ugpair(from_id, v+2)
                to_id = v + 2
            else:
                to_id = v[0]
        self.c.execute("""
            SELECT m_id FROM messages ORDER BY m_id DESC LIMIT 1
        """)
        v = self.c.fetchone()
        if v is None:
            v = 0
        else:
            v = v[0]
        self.c.execute("""
            INSERT INTO messages 
                       (m_id, to_id, from_id, msg)
                       VALUES
                       (?, ?, ?, ?)
                       """, [v + 1, to_id, from_id, msg])
        self.conn.commit()

    @thread_safe
    def get_user_id(self, uname):
        self.c.execute("SELECT u_id FROM users WHERE username=?", [uname])
        v = self.c.fetchone()
        if v is None:
            raise Exception('User does not exist')

        return v[0]

    @thread_safe
    def get_group_id(self, gname):
        self.c.execute("SELECT g_id FROM groups WHERE gname=?", [gname])
        v = self.c.fetchone()
        if v is None:
            raise Exception('Group does not exist')

        return v[0]

    @thread_safe
    def get_messages(self, u_id):
        self.c.execute("""
            SELECT messages.m_id, messages.to_id, messages.from_id, messages.msg
                FROM messages INNER JOIN user_group_pairs ON
                    messages.to_id=user_group_pairs.g_id
                WHERE user_group_pairs.u_id=?
                ORDER BY messages.m_id ASC
            """, [u_id])
        v = self.c.fetchall()
        if v is None:
            raise Exception('No messages')
        return v

    @thread_safe
    def create_group(self, gname):
        self.c.execute("SELECT g_id FROM groups ORDER BY g_id DESC LIMIT 1")
        v = self.c.fetchone()
        if v is None:
            v = 1
        else:
            v = v[0]
        assert (v % 2 == 1)
        self.c.execute("""
            INSERT INTO groups 
                       (g_id, gname)
                       VALUES
                       (?, ?)
                       """, [v + 2, gname])
        self.conn.commit()

    def _insert_ugpair(self, u_id, g_id):
        self.c.execute("SELECT _id FROM user_group_pairs ORDER BY _id DESC LIMIT 1")
        npairs = self.c.fetchone()
        if npairs is None:
            npairs = 0
        else:
            npairs = npairs[0]
        self.c.execute("""
            INSERT INTO user_group_pairs
                       (_id, u_id, g_id)
                       VALUES
                       (?, ?, ?)
                       """, [npairs + 1, u_id, g_id])

    @thread_safe
    def create_account(self, uname):
        self.c.execute("SELECT u_id FROM users ORDER BY u_id DESC LIMIT 1")
        v = self.c.fetchone()
        if v is None:
            v = 0
        else:
            v = v[0]
        assert (v % 2 == 0)
        self.c.execute("""
            INSERT INTO users 
                       (u_id, username)
                       VALUES
                       (?, ?)
                       """, [v + 2, uname])

        self.conn.commit()

    @thread_safe
    def add_group_member(self, gname, uname):
        self.c.execute("SELECT u_id FROM users WHERE username=?", [uname])
        u_id = self.c.fetchone()
        if u_id is None:
            raise Exception('User does not exist')
        else:
            u_id = u_id[0]

        self.c.execute("SELECT g_id FROM groups WHERE gname=?", [gname])
        g_id = self.c.fetchone()
        if g_id is None:
            raise Exception('Group does not exist')
        else:
            g_id = g_id[0]

        self.c.execute("SELECT _id FROM user_group_pairs WHERE u_id=? AND g_id=?",
                       [u_id, g_id])
        v = self.c.fetchone()
        if v is not None and len(v) > 0:
            raise Exception('User already in group')

        self._insert_ugpair(u_id, g_id)
        self.conn.commit()


    @thread_safe
    def remove_account(self, uname):
        self.c.execute("SELECT u_id FROM users WHERE username=?", [uname])
        v = self.c.fetchone()
        if v is None:
            raise Exception("Deleted user doesn't exit")
        else:
            v = v[0]

        self.c.execute("DELETE FROM users WHERE u_id=?", [v])
        self.c.execute("DELETE FROM user_group_pairs WHERE u_id=?", [v])
        self.conn.commit()

    @thread_safe
    def remove_group_member(self, gname, uname):
        self.c.execute("SELECT u_id FROM users WHERE username=?", [uname])
        uid = self.c.fetchone()
        if uid is None:
            raise Exception("User doesn't exist")
        else:
            uid = uid[0]

        self.c.execute("SELECT g_id FROM groups WHERE gname=?", [gname])
        gid = self.c.fetchone()
        if gid is None:
            raise Exception("Group doesn't exist")
        else:
            gid = gid[0]

        self.c.execute("DELETE FROM user_group_pairs WHERE u_id=? AND g_id=?", [uid, gid])
        self.conn.commit()

    @thread_safe
    def edit_group_name(self, gname, newname):
        self.c.execute("UPDATE groups SET gname=? WHERE gname=?", [newname, gname])
        self.conn.commit()

    @thread_safe
    def get_groups(self, pattern):
        self.c.execute("SELECT g_id, gname FROM groups WHERE gname LIKE ?", [pattern])
        v = self.c.fetchall()
        if v is None:
            return []
        return v

    @thread_safe
    def get_accounts(self, pattern):
        self.c.execute("SELECT u_id, username FROM users WHERE username LIKE ? ORDER BY u_id ASC", [pattern])
        v = self.c.fetchall()
        if v is None:
            return []
        return v

    @thread_safe
    def get_group_members(self, gname):
        self.c.execute("""
            SELECT users.u_id, users.username FROM
                users INNER JOIN user_group_pairs ON users.u_id=user_group_pairs.u_id
                INNER JOIN groups ON user_group_pairs.g_id=groups.g_id
                WHERE groups.gname=?""", [gname])
        v = self.c.fetchall()
        if v is None:
            return []
        return v

if __name__ == '__main__':
    db = DBManager()
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
    assert tuple([r[1] for r in res]) == ('composers', 'mathematicians', 'students')

    res = db.get_accounts("______")
    assert tuple([r[1] for r in res]) == ('ludwig', 'johann')

    res = db.get_group_members("composers")
    assert tuple([r[1] for r in res]) == ('ludwig', 'johann', 'wolfgang')


    db.insert_message(db.get_user_id("tslilyai"),
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
        return tuple([l[3] for l in ls])
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
