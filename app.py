from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# Clave secreta necesaria para la protección CSRF de Flask-WTF.
# En un proyecto real esta clave debería venir de una variable de entorno.
app.config['SECRET_KEY'] = 'clave-secreta-proyecto-integrador-dsweb-2026'

# ---------------------------------------------------------------------------
# Datos de ejemplo en memoria (no se requiere base de datos en esta etapa).
# Se definen a nivel de módulo para que los formularios puedan agregar
# nuevos registros mientras la aplicación siga en ejecución.
# ---------------------------------------------------------------------------

lista_productos = [
    {"nombre": "Laptop Empresarial", "categoria": "Tecnología", "precio": 750.00, "stock": 8},
    {"nombre": "Impresora Multifuncional", "categoria": "Tecnología", "precio": 180.50, "stock": 3},
    {"nombre": "Silla Ergonómica", "categoria": "Mobiliario", "precio": 95.00, "stock": 0},
    {"nombre": "Escritorio Ejecutivo", "categoria": "Mobiliario", "precio": 210.00, "stock": 5},
    {"nombre": "Proyector HD", "categoria": "Tecnología", "precio": 320.00, "stock": 0},
    {"nombre": "Archivador Metálico", "categoria": "Mobiliario", "precio": 60.00, "stock": 12},
]

lista_clientes = [
    {"nombre": "María Fernández", "email": "MARIA.FERNANDEZ@gmail.com", "telefono": "0991234567", "activo": True},
    {"nombre": "Carlos Zambrano", "email": "carlos.zambrano@gmail.com", "telefono": "0987654321", "activo": True},
    {"nombre": "Ana Torres", "email": "ANA.TORRES@hotmail.com", "telefono": "0965432198", "activo": False},
    {"nombre": "Luis Andrade", "email": "luis.andrade@gmail.com", "telefono": "0978123456", "activo": True},
    {"nombre": "Paola Rivas", "email": "paola.rivas@outlook.com", "telefono": "0993216547", "activo": False},
]

lista_proveedores = [
    {"nombre": "Distribuidora Andina S.A.", "contacto": "Jorge Salazar", "ciudad": "Guayaquil", "calificacion": 5},
    {"nombre": "Importadora Continental", "contacto": "Diana Mora", "ciudad": "Quito", "calificacion": 3},
    {"nombre": "Suministros del Litoral", "contacto": "Pedro Cevallos", "ciudad": "Manta", "calificacion": 1},
    {"nombre": "Tecno Insumos Cía. Ltda.", "contacto": "Sofía Pincay", "ciudad": "Guayaquil", "calificacion": 4},
]

lista_facturas = [
    {"numero": "F001-2026", "cliente": "María Fernández", "total": 830.50, "estado": "Pagada"},
    {"numero": "F002-2026", "cliente": "Carlos Zambrano", "total": 210.00, "estado": "Pendiente"},
    {"numero": "F003-2026", "cliente": "Luis Andrade", "total": 95.00, "estado": "Pagada"},
    {"numero": "F004-2026", "cliente": "Ana Torres", "total": 320.00, "estado": "Pendiente"},
]


# ---------------------------------------------------------------------------
# Rutas principales (listados) - desarrolladas en semanas anteriores
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html', active='inicio')


@app.route('/productos')
def productos():
    return render_template(
        'productos.html',
        productos=lista_productos,
        titulo_modulo="Productos Registrados",
        active='productos'
    )


@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=lista_clientes, active='clientes')


@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=lista_proveedores, active='proveedores')


@app.route('/facturacion')
def facturacion():
    total_facturado = sum(factura["total"] for factura in lista_facturas)
    return render_template(
        'facturacion.html',
        facturas=lista_facturas,
        total_facturado=total_facturado,
        active='facturacion'
    )


# ---------------------------------------------------------------------------
# Rutas de formularios (Semana 11) - Flask-WTF + WTForms
# ---------------------------------------------------------------------------

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()

    if form.validate_on_submit():
        lista_productos.append({
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data,
        })
        flash('Producto registrado correctamente.', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form, active='productos')


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()

    if form.validate_on_submit():
        lista_clientes.append({
            "nombre": form.nombre.data,
            "email": form.email.data,
            "telefono": form.telefono.data,
            "activo": form.activo.data,
        })
        flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form, active='clientes')


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()

    if form.validate_on_submit():
        lista_proveedores.append({
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "ciudad": form.ciudad.data,
            "calificacion": form.calificacion.data,
        })
        flash('Proveedor registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form, active='proveedores')


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_factura():
    form = FacturacionForm()

    if form.validate_on_submit():
        lista_facturas.append({
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": form.total.data,
            "estado": form.estado.data,
        })
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form, active='facturacion')


if __name__ == '__main__':
    app.run(debug=True)
