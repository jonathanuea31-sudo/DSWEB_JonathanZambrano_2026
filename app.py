from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', active='inicio')


@app.route('/productos')
def productos():
    titulo_modulo = "Productos Registrados"

    productos = [
        {"nombre": "Laptop Empresarial", "categoria": "Tecnología", "precio": 750.00, "stock": 8},
        {"nombre": "Impresora Multifuncional", "categoria": "Tecnología", "precio": 180.50, "stock": 3},
        {"nombre": "Silla Ergonómica", "categoria": "Mobiliario", "precio": 95.00, "stock": 0},
        {"nombre": "Escritorio Ejecutivo", "categoria": "Mobiliario", "precio": 210.00, "stock": 5},
        {"nombre": "Proyector HD", "categoria": "Tecnología", "precio": 320.00, "stock": 0},
        {"nombre": "Archivador Metálico", "categoria": "Mobiliario", "precio": 60.00, "stock": 12},
    ]

    return render_template(
        'productos.html',
        productos=productos,
        titulo_modulo=titulo_modulo,
        active='productos'
    )


@app.route('/clientes')
def clientes():
    clientes = [
        {"nombre": "María Fernández", "email": "MARIA.FERNANDEZ@gmail.com", "telefono": "0991234567", "activo": True},
        {"nombre": "Carlos Zambrano", "email": "carlos.zambrano@gmail.com", "telefono": "0987654321", "activo": True},
        {"nombre": "Ana Torres", "email": "ANA.TORRES@hotmail.com", "telefono": "0965432198", "activo": False},
        {"nombre": "Luis Andrade", "email": "luis.andrade@gmail.com", "telefono": "0978123456", "activo": True},
        {"nombre": "Paola Rivas", "email": "paola.rivas@outlook.com", "telefono": "0993216547", "activo": False},
    ]

    return render_template('clientes.html', clientes=clientes, active='clientes')


@app.route('/proveedores')
def proveedores():
    proveedores = [
        {"nombre": "Distribuidora Andina S.A.", "contacto": "Jorge Salazar", "ciudad": "Guayaquil", "calificacion": 5},
        {"nombre": "Importadora Continental", "contacto": "Diana Mora", "ciudad": "Quito", "calificacion": 3},
        {"nombre": "Suministros del Litoral", "contacto": "Pedro Cevallos", "ciudad": "Manta", "calificacion": 1},
        {"nombre": "Tecno Insumos Cía. Ltda.", "contacto": "Sofía Pincay", "ciudad": "Guayaquil", "calificacion": 4},
    ]

    return render_template('proveedores.html', proveedores=proveedores, active='proveedores')


@app.route('/facturacion')
def facturacion():
    facturas = [
        {"numero": "F001-2026", "cliente": "María Fernández", "total": 830.50, "estado": "Pagada"},
        {"numero": "F002-2026", "cliente": "Carlos Zambrano", "total": 210.00, "estado": "Pendiente"},
        {"numero": "F003-2026", "cliente": "Luis Andrade", "total": 95.00, "estado": "Pagada"},
        {"numero": "F004-2026", "cliente": "Ana Torres", "total": 320.00, "estado": "Pendiente"},
    ]

    total_facturado = sum(factura["total"] for factura in facturas)

    return render_template(
        'facturacion.html',
        facturas=facturas,
        total_facturado=total_facturado,
        active='facturacion'
    )


if __name__ == '__main__':
    app.run(debug=True)
