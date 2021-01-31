import sqlite3
import time


def create_connection(db_file):
    """ Create a connection to sqllite that we can use.
    :param db_file: specifies database file.
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        raise
        return None
    
def insert_checkin(conn, tag):
    """
    Inserts new tag into checkin.
    :param tag: Tag for user to insert
    :param conn: SQL Connection
    :return: ID of row inserted
    """
    userid = get_userid(conn,tag)
    if userid > 0:
        time_stamp = int(time.time())
        sql = '''INSERT INTO checkins(user, checkin) VALUES(?,?)'''
        try:
            cur = conn.cursor()
            cur.execute(sql, (userid, time_stamp))
            conn.commit()
            return cur.lastrowid
        except:
            raise
            return None

def insert_checkout(conn, tag):
    """
    Inserts new tag into checkin.
    :param tag: Tag for user to insert
    :param conn: SQL Connection
    :return: ID of row inserted
    """
    userid = get_userid(conn,tag)
    if userid > 0:
        time_stamp = int(time.time())
        #Get last row of user
        lr_sql = '''SELECT id FROM checkins WHERE user=? ORDER BY id DESC limit 1'''
        
        up_sql = '''UPDATE checkins SET checkout=? WHERE id=?'''
        try:
            cur = conn.cursor()
            cur.execute(lr_sql, (userid,))
            checkin_id = cur.fetchone()[0]
            cur.execute(up_sql, (time_stamp, userid))
            conn.commit()
            return cur.lastrowid
        except:
            raise
            return None

def new_user(conn, tag, email,phone):
    """
    Create new user in users table
    :param conn: SQL Connection
    :param tag: User tag
    :param email: User e-mail
    :param phone: User phone number
    :param phone: User phone number
    :return id: ID of user created. -1 means duplicate tag. -2 other error.
    """
    sql = '''INSERT INTO users(tag,email,phone) VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag, email, phone))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return -1
    else:
        raise
        return -2
        
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
        cur.execute(sql, (tag,))
        return cur.fetchone()[0]
    except:
        return -1
    
