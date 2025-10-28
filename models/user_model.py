
from database import get_connection

def find_by_username(username):
    conn = get_connection()
    row = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    conn.close()
    return row

def get_by_id(id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
    conn.close()
    return row

def create(username, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users(username,password_hash) VALUES (?,?)', (username, password_hash))
    conn.commit()
    last = cur.lastrowid
    conn.close()
    return last
