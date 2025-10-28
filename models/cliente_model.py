
from database import get_connection

def create(nombres, email, telefono):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO clientes(nombres,email,telefono) VALUES (?,?,?)', (nombres,email,telefono))
    conn.commit()
    last = cur.lastrowid
    conn.close()
    return last

def all():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return rows

def get(id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM clientes WHERE id=?', (id,)).fetchone()
    conn.close()
    return row

def update(id, nombres, email, telefono):
    conn = get_connection()
    conn.execute('UPDATE clientes SET nombres=?, email=?, telefono=? WHERE id=?', (nombres,email,telefono,id))
    conn.commit()
    conn.close()

def delete(id):
    conn = get_connection()
    conn.execute('DELETE FROM clientes WHERE id=?', (id,))
    conn.commit()
    conn.close()
