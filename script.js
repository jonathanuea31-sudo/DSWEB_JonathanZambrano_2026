// ======================================
// DATOS DINÁMICOS
// ======================================

const servicios = [

{

titulo:"Gestión de Clientes",

descripcion:"Administración completa de clientes registrados.",

icono:"bi-people"

},

{

titulo:"Control de Productos",

descripcion:"Registro y organización de productos.",

icono:"bi-box-seam"

},

{

titulo:"Reportes",

descripcion:"Generación de reportes y estadísticas.",

icono:"bi-bar-chart-line"

}

];

// ======================================
// MOSTRAR SERVICIOS
// ======================================

const contenedorServicios=document.getElementById("contenedorServicios");

servicios.forEach(servicio=>{

contenedorServicios.innerHTML+=`

<div class="col-md-4 mb-4">

<div class="card h-100 shadow">

<div class="card-body text-center">

<div class="icon-badge">
<i class="bi ${servicio.icono}"></i>
</div>

<h4>${servicio.titulo}</h4>

<p>${servicio.descripcion}</p>

</div>

</div>

</div>

`;

});

// ======================================
// REGISTROS
// ======================================

let registros=[];

const formulario=document.getElementById("formulario");

const nombre=document.getElementById("nombre");

const categoria=document.getElementById("categoria");

const descripcion=document.getElementById("descripcion");

const lista=document.getElementById("listaRegistros");

const contador=document.getElementById("contador");

const estado=document.getElementById("estadoRegistros");

const mensaje=document.getElementById("mensajeGeneral");

const spinnerCarga=document.getElementById("spinnerCarga");

// ======================================
// VALIDACIONES
// ======================================

function validarNombre(){

if(nombre.value.trim().length<3){

nombre.classList.add("is-invalid");

nombre.classList.remove("is-valid");

document.getElementById("errorNombre").textContent="Ingrese mínimo 3 caracteres.";

return false;

}

nombre.classList.remove("is-invalid");

nombre.classList.add("is-valid");

document.getElementById("errorNombre").textContent="";

return true;

}

function validarCategoria(){

if(categoria.value===""){

categoria.classList.add("is-invalid");

categoria.classList.remove("is-valid");

document.getElementById("errorCategoria").textContent="Seleccione una categoría.";

return false;

}

categoria.classList.remove("is-invalid");

categoria.classList.add("is-valid");

document.getElementById("errorCategoria").textContent="";

return true;

}

function validarDescripcion(){

if(descripcion.value.trim().length<10){

descripcion.classList.add("is-invalid");

descripcion.classList.remove("is-valid");

document.getElementById("errorDescripcion").textContent="La descripción debe tener mínimo 10 caracteres.";

return false;

}

descripcion.classList.remove("is-invalid");

descripcion.classList.add("is-valid");

document.getElementById("errorDescripcion").textContent="";

return true;

}
// ======================================
// EVENTOS EN TIEMPO REAL
// ======================================

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

// ======================================
// MOSTRAR REGISTROS
// ======================================

function mostrarRegistros(){

lista.innerHTML="";

contador.textContent=registros.length;

if(registros.length===0){

estado.innerHTML=`
<div class="alert alert-warning text-center">
No existen registros todavía.
</div>
`;

return;

}

estado.innerHTML=`
<div class="alert alert-success text-center">
Existen ${registros.length} registros almacenados.
</div>
`;

registros.forEach((registro,index)=>{

lista.innerHTML+=`

<div class="col-md-4 mb-4">

<div class="card registro-card h-100 shadow">

<div class="card-body">

<div class="d-flex justify-content-between align-items-start mb-2">

<h4 class="mb-0">${registro.nombre}</h4>

<span class="badge-categoria">${registro.categoria}</span>

</div>

<p>${registro.descripcion}</p>

<button
class="btn btn-outline-primary w-100 mb-2"
onclick="verDetalle(${index})">

Ver Detalle

</button>

<button
class="btn btn-danger w-100"
onclick="eliminarRegistro(${index})">

Eliminar

</button>

</div>

</div>

</div>

`;

});

}

// ======================================
// VER DETALLE (MODAL)
// ======================================

function verDetalle(indice){

const registro=registros[indice];

document.getElementById("modalDetalleBody").innerHTML=`

<p><strong>Nombre:</strong> ${registro.nombre}</p>

<p><strong>Categoría:</strong> ${registro.categoria}</p>

<p><strong>Descripción:</strong> ${registro.descripcion}</p>

`;

const modal=new bootstrap.Modal(document.getElementById("modalDetalle"));

modal.show();

}

// ======================================
// REGISTRAR
// ======================================

formulario.addEventListener("submit",function(e){

e.preventDefault();

const okNombre=validarNombre();
const okCategoria=validarCategoria();
const okDescripcion=validarDescripcion();

if(!(okNombre && okCategoria && okDescripcion)){

mensaje.innerHTML=`
<div class="alert alert-danger">
Revise los campos del formulario.
</div>
`;

return;

}

const nuevoRegistro={

nombre:nombre.value,

categoria:categoria.value,

descripcion:descripcion.value

};

// Muestra el spinner mientras se "procesa" el registro
mensaje.innerHTML="";
spinnerCarga.classList.remove("d-none");

setTimeout(function(){

registros.push(nuevoRegistro);

spinnerCarga.classList.add("d-none");

mensaje.innerHTML=`
<div class="alert alert-success">
Registro agregado correctamente.
</div>
`;

formulario.reset();

nombre.classList.remove("is-valid");
categoria.classList.remove("is-valid");
descripcion.classList.remove("is-valid");

mostrarRegistros();

},900);

});

// ======================================
// ELIMINAR
// ======================================

function eliminarRegistro(indice){

registros.splice(indice,1);

mostrarRegistros();

}

// ======================================
// INICIO
// ======================================

mostrarRegistros();