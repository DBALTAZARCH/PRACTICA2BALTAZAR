
from database import get_connection

def all():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM paquetes').fetchall()
    conn.close()
    return rows

def get_by_id(id_destino):
    conn = get_connection()
    row = conn.execute('SELECT * FROM paquetes WHERE id_destino=?', (id_destino,)).fetchone()
    conn.close()
    return row

def create(nombre, precio):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO paquetes(nombre,precio) VALUES (?,?)', (nombre, precio))
    conn.commit()
    last = cur.lastrowid
    conn.close()
    return last

def update(id_destino, nombre, precio):
    conn = get_connection()
    conn.execute('UPDATE paquetes SET nombre=?, precio=? WHERE id_destino=?', (nombre, precio, id_destino))
    conn.commit()
    conn.close()

def delete(id_destino):
    conn = get_connection()
    conn.execute('DELETE FROM paquetes WHERE id_destino=?', (id_destino,))
    conn.commit()
    conn.close()
