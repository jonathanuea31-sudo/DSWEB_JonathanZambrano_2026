import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/dsweb")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        usuario VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS proveedores (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        contacto VARCHAR(80) NOT NULL,
        ciudad VARCHAR(60) NOT NULL,
        calificacion INTEGER NOT NULL CHECK (calificacion BETWEEN 1 AND 5)
    );
    CREATE TABLE IF NOT EXISTS clientes (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        activo BOOLEAN NOT NULL DEFAULT TRUE
    );
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(80) NOT NULL,
        categoria VARCHAR(60) NOT NULL,
        precio NUMERIC(10,2) NOT NULL CHECK (precio > 0),
        stock INTEGER NOT NULL CHECK (stock >= 0),
        proveedor_id INTEGER REFERENCES proveedores(id) ON DELETE SET NULL
    );
    CREATE TABLE IF NOT EXISTS facturas (
        id SERIAL PRIMARY KEY,
        numero VARCHAR(20) UNIQUE NOT NULL,
        cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
        total NUMERIC(10,2) NOT NULL CHECK (total > 0),
        estado VARCHAR(20) NOT NULL
    );
    """)
    cur.execute("SELECT COUNT(*) AS total FROM proveedores")
    if cur.fetchone()["total"] == 0:
        cur.executemany("INSERT INTO proveedores(nombre,contacto,ciudad,calificacion) VALUES(%s,%s,%s,%s)", [
            ("Distribuidora Andina S.A.","Jorge Salazar","Guayaquil",5),
            ("Importadora Continental","Diana Mora","Quito",3)])
    cur.execute("SELECT COUNT(*) AS total FROM clientes")
    if cur.fetchone()["total"] == 0:
        cur.executemany("INSERT INTO clientes(nombre,email,telefono,activo) VALUES(%s,%s,%s,%s)", [
            ("María Fernández","maria.fernandez@gmail.com","0991234567",True),
            ("Carlos Zambrano","carlos.zambrano@gmail.com","0987654321",True)])
    cur.execute("SELECT COUNT(*) AS total FROM productos")
    if cur.fetchone()["total"] == 0:
        cur.executemany("INSERT INTO productos(nombre,categoria,precio,stock) VALUES(%s,%s,%s,%s)", [
            ("Laptop Empresarial","Tecnología",750,8),
            ("Impresora Multifuncional","Tecnología",180.50,3),
            ("Silla Ergonómica","Mobiliario",95,0)])
    conn.commit()
    cur.close(); conn.close()
