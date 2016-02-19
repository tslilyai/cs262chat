'''
This file contains all functions necessary for the server to interface with the database!
'''

import sqlite3

class DBManager(object):
    def __init__(self):
        self.conn = sqlite3.connect('chatapp.db')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        self.c.execute("""
            CREATE TABLE users (u_id int NOT NULL PRIMARY KEY, username varchar(255) UNIQUE)
        """)
        self.c.execute("""
            CREATE TABLE groups (g_id int NOT NULL PRIMARY KEY, gname varchar(255) UNIQUE)
        """)
        self.c.execute("""
            CREATE TABLE user_group_pairs (_id int NOT NULL PRIMARY KEY, u_id int, g_id int)
        """)
        self.c.execute("""
            CREATE TABLE messages (m_id int NOT NULL PRIMARY KEY, to_id int, from_id int, msg varchar(1023))
        """)
        self.conn.commit()

    def insert_message(self, to_id, from_id, msg):
        if len(msg) > 1023:
            raise Exception('Message string too long')
        # TODO: check validity of to_id and from_id
        self.c.execute("""
            SELECT m_id from messages ORDER BY m_id DESC LIMIT 1
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


if __name__ == '__main__':
    db = DBManager()
    db.create_tables()
    db.insert_message(1, 1, "Hello world!")
    db.insert_message(1, 1, "Hello world!")
