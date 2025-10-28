
import sqlite3, os
from flask import current_app

def get_connection():
    db_path = current_app.config.get('DB_PATH')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    db_path = app.config.get('DB_PATH')
    if not os.path.exists(db_path):
        with app.app_context():
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            # create tables
            c.execute('''
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                email TEXT,
                telefono TEXT
            );
            ''')
            c.execute('''
            CREATE TABLE paquetes (
                id_destino INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            );
            ''')
            c.execute('''
            CREATE TABLE reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_clientes INTEGER,
                id_paquete INTEGER,
                fecha_reserva TEXT,
                FOREIGN KEY(id_clientes) REFERENCES clientes(id),
                FOREIGN KEY(id_paquete) REFERENCES paquetes(id_destino)
            );
            ''')
            c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            ''')
            # seed sample paquetes
            c.executemany('INSERT INTO paquetes(nombre, precio) VALUES (?, ?);', [
                ('La Paz Tour', 120.0),
                ('Copacabana Excursion', 80.0),
                ('Salar de Uyuni 3D/2N', 350.0),
            ])
            # create default admin user: username admin, password admin (hashed below)
            import hashlib
            pw = hashlib.sha256('admin'.encode('utf-8')).hexdigest()
            c.execute('INSERT INTO users(username,password_hash) VALUES (?,?);', ('admin', pw))
            conn.commit()
            conn.close()
