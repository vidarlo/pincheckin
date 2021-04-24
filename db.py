#    BFK Pinball Player Checkin system
#    Copyright (C) 2021 Vidar Løkken <vl@bitsex.net>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sqlite3
import time
import datetime
import server
import azure_sql
import pyodbc


def create_connection():
    """ Create a connection to database that we can use.
    :return: Connection object or None
    """
    conn = None
    try:
        connstring, tokenstruct, tokenopt = azure_sql.get_connstring()
        print(connstring)
        print(tokenstruct)
        print(tokenopt)
        conn = pyodbc.connect(connstring, attrs_before = { tokenopt:tokenstruct})
        return conn
    except Error as e:
        print(e)
        raise

    
def insert_checkin(conn, tag):
    """
    Inserts new tag into checkin.
    :param tag: Tag for user to insert
    :param conn: SQL Connection
    :return: ID of row inserted
    """
    userid = get_userid(conn,tag.upper())
    if userid > 0:
        sql = '''SELECT checkout FROM checkins WHERE user=? AND checkout is null'''
        cur = conn.cursor()
        cur.execute(sql, (userid,))
        data=cur.fetchall()
        if len(data)==0:
            sql = '''INSERT INTO checkins(user, checkin) VALUES(?,?)'''
            try:
                cur = conn.cursor()
                time_stamp = int(time.time())
                cur.execute(sql, (userid, time_stamp))
                conn.commit()
                return cur.lastrowid
            except:
                raise
        else:
            #Open checkins...
            return -1
    else:
        #No such user
        return -2
                

def insert_checkout(conn, tag):
    """
    Inserts new tag into checkin.
    :param tag: Tag for user to insert
    :param conn: SQL Connection
    :return: ID of row inserted
    """
    userid = get_userid(conn,tag.upper())
    if userid > 0:
        time_stamp = int(time.time())
        #Get last row of user
        lr_sql = '''SELECT id FROM checkins WHERE user=? ORDER BY id DESC limit 1'''
        
        up_sql = '''UPDATE checkins SET checkout=? WHERE id=?'''
        try:
            cur = conn.cursor()
            cur.execute(lr_sql, (userid,))
            checkin_id = cur.fetchone()[0]
            cur.execute(up_sql, (time_stamp, checkin_id))
            last_id = checkin_id
            conn.commit()
            return last_id
        except:
            raise
            return None
    

def new_user(conn, tag, email,phone, name):
    """
    Create new user in users table
    :param conn: SQL Connection
    :param tag: User tag
    :param email: User e-mail
    :param name: User's name
    :param phone: User phone number
    :param phone: User phone number
    :return id: ID of user created. -1 means duplicate tag. -2 other error.
    """
    sql = '''INSERT INTO users(tag,email,phone, name) VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag.upper(), email, phone, name))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return -1
    else:
        raise
        return -2


def insert_guest_checkin(conn, email,phone, name):
    """
    Inserts new entry in guest_checkins.
    :param name: name of user
    :param conn: SQL Connection
    

    """
    sql = '''INSERT INTO guest_checkins(email,phone, name, time_stamp) VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        time_stamp = int(time.time())
        cur.execute(sql, (email, phone, name, time_stamp))
        conn.commit()
    except sqlite3.IntegrityError:
        return -1
        
def get_userid(conn,tag):
    """
    Get user id from tag
    :param conn: SQL Connection
    :param tag: User tag
    :return id: User ID or -1 for unknown user
    """
    sql = '''SELECT id FROM users WHERE tag=?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag.upper(),))
        return cur.fetchone()[0]
    except:
        return -1

def get_usertag(conn,serial):
    """
    Get user id from tag
    :param conn: SQL Connection
    :param tag: User tag
    :return id: User ID or -1 for unknown user
    """
    sql = '''SELECT tag FROM users WHERE serial=?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (serial,))
        return cur.fetchone()[0]
    except:
        return -1

def get_name(conn,tag):
    """
    Get user name from tag
    :param conn: SQL Connection
    :param tag: User tag
    :return name: User ID or -1 for unknown user
    """
    sql = '''SELECT name FROM users WHERE tag=?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag.upper(),))
        return cur.fetchone()[0]
    except:
        return -1
    
def get_entries(conn,start = 0,count = 25, checkedin = False):
    """
    Get entries
    :param conn: SQL Connection
    :param start: Start point (default:0)
    :param count: number to get (default: 25)
    :param checkedin: Only return checked in users if true
    """
    sql = None
    if not checkedin:
        sql = '''SELECT users.tag,checkins.checkin,checkins.checkout FROM checkins INNER JOIN users on users.id = checkins.user ORDER BY checkins.id DESC LIMIT ?,?'''
    elif checkedin:
        sql = '''SELECT users.tag,checkins.checkin FROM checkins INNER JOIN users on users.id = checkins.user WHERE checkins.checkout is null ORDER BY checkins.id DESC LIMIT ?,?'''  
    try:
        cur = conn.cursor()
        cur.execute(sql, (start,count))
        return cur.fetchall()
    except:
        raise

