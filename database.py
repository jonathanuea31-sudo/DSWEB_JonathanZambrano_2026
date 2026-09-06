"""
Módulo de conexión a la base de datos SQLite del proyecto.

Se centraliza aquí la ruta de la base de datos, la creación de la conexión
y la inicialización de las tablas, para mantener app.py más limpio y
facilitar la futura migración hacia MySQL o PostgreSQL sin reorganizar
el resto del proyecto.
"""

import os
import sqlite3

# Carpeta 'data/' en la raíz del proyecto, y archivo ferreteria.db dentro de ella.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'ferreteria.db')


def get_db_connection():
    """Crea y devuelve una conexión a la base de datos SQLite.

    row_factory = sqlite3.Row permite acceder a las columnas por nombre
    (ej. fila['nombre']), lo cual además es compatible con la notación
    de punto de Jinja2 (ej. {{ producto.nombre }}).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea la carpeta data/ y la tabla de productos si todavía no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.commit()

    # Si la tabla está vacía (primera vez que se crea la base de datos),
    # se insertan algunos productos de ejemplo para no arrancar vacío.
    cantidad = conn.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    if cantidad == 0:
        productos_iniciales = [
            ("Laptop Empresarial", "Tecnología", 750.00, 8),
            ("Impresora Multifuncional", "Tecnología", 180.50, 3),
            ("Silla Ergonómica", "Mobiliario", 95.00, 0),
            ("Escritorio Ejecutivo", "Mobiliario", 210.00, 5),
            ("Proyector HD", "Tecnología", 320.00, 0),
            ("Archivador Metálico", "Mobiliario", 60.00, 12),
        ]
        conn.executemany(
            'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
            productos_iniciales
        )
        conn.commit()

    conn.close()
