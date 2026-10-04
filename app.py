import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from database import get_db_connection, init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave-secreta-dsweb-2026")
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Inicia sesión para continuar."

try:
    init_db()
except Exception:
    pass

class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]; self.usuario = row["usuario"]

@login_manager.user_loader
def load_user(user_id):
    conn=get_db_connection(); cur=conn.cursor()
    cur.execute("SELECT id,usuario FROM usuarios WHERE id=%s",(user_id,))
    row=cur.fetchone(); cur.close(); conn.close()
    return User(row) if row else None

@app.route("/")
def index(): return render_template("index.html", active="inicio")

@app.route("/registro", methods=["GET","POST"])
def registro():
    if request.method=="POST":
        usuario=request.form.get("usuario","").strip(); password=request.form.get("password","")
        if len(usuario)<3 or len(password)<6:
            flash("El usuario debe tener 3 caracteres y la contraseña 6.","danger")
        else:
            conn=get_db_connection(); cur=conn.cursor()
            try:
                cur.execute("INSERT INTO usuarios(usuario,password) VALUES(%s,%s)",(usuario,generate_password_hash(password)))
                conn.commit(); flash("Usuario registrado. Ya puedes iniciar sesión.","success"); return redirect(url_for("login"))
            except Exception:
                conn.rollback(); flash("El usuario ya existe.","danger")
            finally: cur.close(); conn.close()
    return render_template("registro.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        conn=get_db_connection(); cur=conn.cursor()
        cur.execute("SELECT id,usuario,password FROM usuarios WHERE usuario=%s",(request.form.get("usuario","").strip(),))
        row=cur.fetchone(); cur.close(); conn.close()
        if row and check_password_hash(row["password"],request.form.get("password","")):
            login_user(User(row)); return redirect(url_for("index"))
        flash("Usuario o contraseña incorrectos.","danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user(); flash("Sesión cerrada.","success"); return redirect(url_for("login"))

@app.route("/productos")
@login_required
def productos():
    conn=get_db_connection(); cur=conn.cursor()
    cur.execute("SELECT p.*, pr.nombre AS proveedor_nombre FROM productos p LEFT JOIN proveedores pr ON pr.id=p.proveedor_id ORDER BY p.id DESC")
    rows=cur.fetchall(); cur.close(); conn.close()
    return render_template("productos.html",productos=rows,titulo_modulo="Productos Registrados",active="productos")

@app.route("/productos/nuevo",methods=["GET","POST"])
@login_required
def nuevo_producto():
    form=ProductoForm()
    if form.validate_on_submit():
        conn=get_db_connection(); cur=conn.cursor()
        cur.execute("INSERT INTO productos(nombre,categoria,precio,stock) VALUES(%s,%s,%s,%s)",(form.nombre.data,form.categoria.data,form.precio.data,form.stock.data))
        conn.commit(); cur.close(); conn.close(); flash("Producto registrado.","success"); return redirect(url_for("productos"))
    return render_template("formulario_producto.html",form=form,active="productos")

@app.route("/productos/eliminar/<int:id>",methods=["POST"])
@login_required
def eliminar_producto(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("DELETE FROM productos WHERE id=%s",(id,)); conn.commit(); cur.close(); conn.close(); flash("Producto eliminado.","success"); return redirect(url_for("productos"))

@app.route("/productos/editar/<int:id>",methods=["GET","POST"])
@login_required
def editar_producto(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT * FROM productos WHERE id=%s",(id,)); row=cur.fetchone()
    if not row: cur.close(); conn.close(); flash("Producto no encontrado.","danger"); return redirect(url_for("productos"))
    form=ProductoForm(obj=row)
    if form.validate_on_submit():
        cur.execute("UPDATE productos SET nombre=%s,categoria=%s,precio=%s,stock=%s WHERE id=%s",(form.nombre.data,form.categoria.data,form.precio.data,form.stock.data,id))
        conn.commit(); cur.close(); conn.close(); flash("Producto actualizado.","success"); return redirect(url_for("productos"))
    cur.close(); conn.close(); return render_template("formulario_producto.html",form=form,active="productos")

@app.route("/clientes")
@login_required
def clientes():
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT * FROM clientes ORDER BY id DESC")
    rows=cur.fetchall(); cur.close(); conn.close(); return render_template("clientes.html",clientes=rows,active="clientes")

@app.route("/clientes/nuevo",methods=["GET","POST"])
@login_required
def nuevo_cliente():
    form=ClienteForm()
    if form.validate_on_submit():
        conn=get_db_connection(); cur=conn.cursor(); cur.execute("INSERT INTO clientes(nombre,email,telefono,activo) VALUES(%s,%s,%s,%s)",(form.nombre.data,form.email.data,form.telefono.data,form.activo.data)); conn.commit(); cur.close(); conn.close(); flash("Cliente registrado.","success"); return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html",form=form,active="clientes")

@app.route("/clientes/eliminar/<int:id>",methods=["POST"])
@login_required
def eliminar_cliente(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("DELETE FROM clientes WHERE id=%s",(id,)); conn.commit(); cur.close(); conn.close(); flash("Cliente eliminado.","success"); return redirect(url_for("clientes"))

@app.route("/clientes/editar/<int:id>",methods=["GET","POST"])
@login_required
def editar_cliente(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT * FROM clientes WHERE id=%s",(id,)); row=cur.fetchone()
    if not row: cur.close(); conn.close(); return redirect(url_for("clientes"))
    form=ClienteForm(obj=row)
    if form.validate_on_submit():
        cur.execute("UPDATE clientes SET nombre=%s,email=%s,telefono=%s,activo=%s WHERE id=%s",(form.nombre.data,form.email.data,form.telefono.data,form.activo.data,id)); conn.commit(); cur.close(); conn.close(); flash("Cliente actualizado.","success"); return redirect(url_for("clientes"))
    cur.close(); conn.close(); return render_template("formulario_cliente.html",form=form,active="clientes")

@app.route("/proveedores")
@login_required
def proveedores():
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT * FROM proveedores ORDER BY id DESC")
    rows=cur.fetchall(); cur.close(); conn.close(); return render_template("proveedores.html",proveedores=rows,active="proveedores")

@app.route("/proveedores/nuevo",methods=["GET","POST"])
@login_required
def nuevo_proveedor():
    form=ProveedorForm()
    if form.validate_on_submit():
        conn=get_db_connection(); cur=conn.cursor(); cur.execute("INSERT INTO proveedores(nombre,contacto,ciudad,calificacion) VALUES(%s,%s,%s,%s)",(form.nombre.data,form.contacto.data,form.ciudad.data,form.calificacion.data)); conn.commit(); cur.close(); conn.close(); flash("Proveedor registrado.","success"); return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html",form=form,active="proveedores")

@app.route("/proveedores/eliminar/<int:id>",methods=["POST"])
@login_required
def eliminar_proveedor(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("DELETE FROM proveedores WHERE id=%s",(id,)); conn.commit(); cur.close(); conn.close(); flash("Proveedor eliminado.","success"); return redirect(url_for("proveedores"))

@app.route("/proveedores/editar/<int:id>",methods=["GET","POST"])
@login_required
def editar_proveedor(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT * FROM proveedores WHERE id=%s",(id,)); row=cur.fetchone()
    if not row: cur.close(); conn.close(); return redirect(url_for("proveedores"))
    form=ProveedorForm(obj=row)
    if form.validate_on_submit():
        cur.execute("UPDATE proveedores SET nombre=%s,contacto=%s,ciudad=%s,calificacion=%s WHERE id=%s",(form.nombre.data,form.contacto.data,form.ciudad.data,form.calificacion.data,id)); conn.commit(); cur.close(); conn.close(); flash("Proveedor actualizado.","success"); return redirect(url_for("proveedores"))
    cur.close(); conn.close(); return render_template("formulario_proveedor.html",form=form,active="proveedores")

@app.route("/facturacion")
@login_required
def facturacion():
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT f.*,c.nombre AS cliente_nombre FROM facturas f JOIN clientes c ON c.id=f.cliente_id ORDER BY f.id DESC")
    rows=cur.fetchall(); total=sum(float(x["total"]) for x in rows); cur.close(); conn.close(); return render_template("facturacion.html",facturas=rows,total_facturado=total,active="facturacion")

@app.route("/facturacion/nueva",methods=["GET","POST"])
@login_required
def nueva_factura():
    form=FacturacionForm(); conn=get_db_connection(); cur=conn.cursor(); cur.execute("SELECT id,nombre FROM clientes ORDER BY nombre"); clientes=cur.fetchall()
    if form.validate_on_submit():
        cur.execute("INSERT INTO facturas(numero,cliente_id,total,estado) VALUES(%s,%s,%s,%s)",(form.numero.data,request.form.get("cliente_id"),form.total.data,form.estado.data)); conn.commit(); cur.close(); conn.close(); flash("Factura registrada.","success"); return redirect(url_for("facturacion"))
    cur.close(); conn.close(); return render_template("formulario_facturacion.html",form=form,clientes=clientes,active="facturacion")

@app.route("/facturacion/eliminar/<int:id>",methods=["POST"])
@login_required
def eliminar_factura(id):
    conn=get_db_connection(); cur=conn.cursor(); cur.execute("DELETE FROM facturas WHERE id=%s",(id,)); conn.commit(); cur.close(); conn.close(); flash("Factura eliminada.","success"); return redirect(url_for("facturacion"))

if __name__=="__main__":
    app.run(debug=False,use_reloader=False)
