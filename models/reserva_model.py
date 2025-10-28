
from database import get_connection

def create(id_cliente, id_paquete, fecha):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO reservas(id_clientes,id_paquete,fecha_reserva) VALUES (?,?,?)', (id_cliente,id_paquete,fecha))
    conn.commit()
    last = cur.lastrowid
    conn.close()
    return last

def ventas_por_destino():
    conn = get_connection()
    rows = conn.execute('''
        SELECT p.id_destino, p.nombre, p.precio, COUNT(r.id_reserva) as total_reservas,
               (COUNT(r.id_reserva) * p.precio) as total_ventas
        FROM paquetes p
        LEFT JOIN reservas r ON p.id_destino = r.id_paquete
        GROUP BY p.id_destino, p.nombre, p.precio
    ''').fetchall()
    conn.close()
    return rows

def all():
    conn = get_connection()
    rows = conn.execute('SELECT r.*, c.nombres as cliente, p.nombre as paquete FROM reservas r LEFT JOIN clientes c ON r.id_clientes=c.id LEFT JOIN paquetes p ON r.id_paquete=p.id_destino ORDER BY r.fecha_reserva DESC').fetchall()
    conn.close()
    return rows

def delete(id_reserva):
    conn = get_connection()
    conn.execute('DELETE FROM reservas WHERE id_reserva=?', (id_reserva,))
    conn.commit()
    conn.close()
