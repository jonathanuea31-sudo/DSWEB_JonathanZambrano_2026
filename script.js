// ===============================
// VARIABLES
// ===============================

const formulario = document.getElementById("formulario");
const nombre = document.getElementById("nombre");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");

const errorNombre = document.getElementById("errorNombre");
const errorCategoria = document.getElementById("errorCategoria");
const errorDescripcion = document.getElementById("errorDescripcion");

const mensajeGeneral = document.getElementById("mensajeGeneral");

const listaRegistros = document.getElementById("listaRegistros");
const contador = document.getElementById("contador");

let registros = [];

// ===============================
// VALIDAR NOMBRE
// ===============================

function validarNombre(){

    if(nombre.value.trim()===""){

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        errorNombre.innerHTML="El nombre es obligatorio.";

        return false;

    }

    if(nombre.value.trim().length<5){

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        errorNombre.innerHTML="Debe tener mínimo 5 caracteres.";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.innerHTML="";

    return true;

}

// ===============================
// VALIDAR CATEGORÍA
// ===============================

function validarCategoria(){

    if(categoria.value===""){

        categoria.classList.remove("is-valid");
        categoria.classList.add("is-invalid");

        errorCategoria.innerHTML="Seleccione una categoría.";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.innerHTML="";

    return true;

}

// ===============================
// VALIDAR DESCRIPCIÓN
// ===============================

function validarDescripcion(){

    if(descripcion.value.trim()===""){

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        errorDescripcion.innerHTML="La descripción es obligatoria.";

        return false;

    }

    if(descripcion.value.trim().length<15){

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        errorDescripcion.innerHTML="Debe contener al menos 15 caracteres.";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.innerHTML="";

    return true;

}

// ===============================
// EVENTOS INPUT
// ===============================

nombre.addEventListener("input",validarNombre);

categoria.addEventListener("input",validarCategoria);

descripcion.addEventListener("input",validarDescripcion);

// ===============================
// EVENTOS BLUR
// ===============================

nombre.addEventListener("blur",validarNombre);

categoria.addEventListener("blur",validarCategoria);

descripcion.addEventListener("blur",validarDescripcion);

// ===============================
// SUBMIT
// ===============================

formulario.addEventListener("submit",function(e){

    e.preventDefault();

    let nombreValido=validarNombre();
    let categoriaValida=validarCategoria();
    let descripcionValida=validarDescripcion();

    if(nombreValido && categoriaValida && descripcionValida){

        registrar();

    }else{

        mensajeGeneral.innerHTML=`

        <div class="alert alert-danger">

        Corrija los errores antes de continuar.

        </div>

        `;

    }

});
// ===============================
// REGISTRAR INFORMACIÓN
// ===============================

function registrar() {

    const registro = {

        nombre: nombre.value.trim(),

        categoria: categoria.value,

        descripcion: descripcion.value.trim()

    };

    registros.push(registro);

    mostrarRegistros();

    formulario.reset();

    nombre.classList.remove("is-valid");
    categoria.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");

    mensajeGeneral.innerHTML = `

        <div class="alert alert-success">

            Registro agregado correctamente.

        </div>

    `;

}

// ===============================
// MOSTRAR REGISTROS
// ===============================

function mostrarRegistros() {

    listaRegistros.innerHTML = "";

    registros.forEach(function(registro, indice) {

        listaRegistros.innerHTML += `

        <tr>

            <td>${registro.nombre}</td>

            <td>${registro.categoria}</td>

            <td>${registro.descripcion}</td>

            <td>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="eliminarRegistro(${indice})">

                    Eliminar

                </button>

            </td>

        </tr>

        `;

    });

    contador.textContent = registros.length;

}

// ===============================
// ELIMINAR REGISTRO
// ===============================

function eliminarRegistro(indice) {

    registros.splice(indice, 1);

    mostrarRegistros();

    mensajeGeneral.innerHTML = `

        <div class="alert alert-warning">

            Registro eliminado correctamente.

        </div>

    `;

}

// ===============================
// LIMPIAR MENSAJES CUANDO EL USUARIO
// COMIENCE A ESCRIBIR NUEVAMENTE
// ===============================

formulario.addEventListener("input", function () {

    mensajeGeneral.innerHTML = "";

});

// ===============================
// CONTADOR INICIAL
// ===============================

contador.textContent = registros.length;