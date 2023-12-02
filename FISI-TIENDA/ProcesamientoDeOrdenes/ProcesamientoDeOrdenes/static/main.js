let articulos = []
let imagenes = [
    "/static/img/cuaderno.jpg",
    "/static/img/lapiz.jpg",
    "/static/img/lapicero.png",
    "/static/img/regla.jpg",
    "/static/img/borrador.png",
    "/static/img/tajador.png",
    "/static/img/mochila.jpg",
    "/static/img/cartuchera.jpeg",
    "/static/img/calculadora.jpeg",
    "/static/img/estuche_reglas.jpg",
    "/static/img/libro_mate.jpg",
    "/static/img/diccionario.jpeg",
    "/static/img/cuaderno_dibujo.jpeg",
    "/static/img/folder_manila.jpg",
    "/static/img/tijeras.jpg",
    "/static/img/cinta.png",
    "/static/img/cola_pequeña.jpg",
    "/static/img/resaltador.jpg",
    "/static/img/compas.png",
    "/static/img/goma_barra.jpg",
]


let data_log = null;


window.addEventListener('DOMContentLoaded', async () => {
    const respuesta = await fetch('/api/articulos');
    const data = await respuesta.json()

    const respuesta_log = await fetch('/api/verificar-sesion'); // Endpoint para verificar la sesión
    data_log = await respuesta_log.json();

    
    articulos = data


    renderArticulo(articulos)

    if (data_log != null) {
        quitarAccesos();
        mostrarMensajeBienvenida(data_log.Nombre+" "+data_log.Apellido); // Mostrar bienvenida si el usuario está logeado
    } else {
        darAccesos();
    }
    agregarEventListeners()
})

function renderArticulo(articulos) {
    const listaArticulos = document.querySelector('#listaArticulos')
    listaArticulos.innerHTML = ''
    
    pos = 0
    articulos.forEach(articulo => {
        const articuloItem = document.createElement('div') // Cambio a div en lugar de li
        articuloItem.classList.add('item') // Añadir la clase 'item'
        articuloItem.innerHTML = `
            <span class="titulo-item">${articulo.Descripcion}</span>
            <span class="id-item">${articulo.ID_Articulo}</span>
            <img src="${imagenes[pos]}" alt="" class="img-item">
            <span class="precio-item">S/ ${articulo.precio_unitario}</span>
            <button class="boton-item">Agregar al Carrito</button>
        `
        console.log(articulo)
        listaArticulos.append(articuloItem)
        pos++
    })
}


function agregarEventListeners() {
    const botonesAgregarAlCarrito = document.querySelectorAll('.boton-item');
    botonesAgregarAlCarrito.forEach(button => {
        button.addEventListener('click', agregarAlCarritoClicked);
    });
}
//------------------------------------------------------------------------------------------------
function cerrarSesion() {
    fetch('/api/cerrar-sesion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ })
    })
    window.location.reload();
}

function mostrarMensajeBienvenida(nombreUsuario) {
    document.querySelector('.registro-form').style.display = 'none';
    document.querySelector('.login-form').style.display = 'none';

    const mensajeBienvenida = document.getElementById('mensajeBienvenida');
    mensajeBienvenida.innerText = `Bienvenido, ${nombreUsuario}!`;
    document.querySelector('.bienvenida').style.display = 'block';
}
function quitarAccesos(){
    document.querySelector('.user-section').style.display = 'none'; 
}
function darAccesos(){
    document.querySelector('.user-section').style.display = 'block'; 
}

function mostrarFormularioRegistro() {
    var registroForm = document.querySelector('.registro-form');
    var estiloRegistro = window.getComputedStyle(registroForm);

    if (estiloRegistro.display === 'none'){
        document.querySelector('.login-form').style.display = 'none';
        registroForm.style.display = 'block';
    } else {
        document.querySelector('.login-form').style.display = 'none';
        registroForm.style.display = 'none';
    }
}

function mostrarFormularioLogin() {
    var registroForm = document.querySelector('.login-form');
    var estiloRegistro = window.getComputedStyle(registroForm);

    if (estiloRegistro.display === 'none'){
        document.querySelector('.registro-form').style.display = 'none';
        registroForm.style.display = 'block';
    } else {
        document.querySelector('.registro-form').style.display = 'none';
        registroForm.style.display = 'none';
    }
}
//------------------------------------------------------------------------------------------------
function registrar() {
    const nombres = document.getElementById('registroNombres').value;
    const apellidos = document.getElementById('registroApellidos').value;
    const correo = document.getElementById('registroCorreo').value;
    const contrasena = document.getElementById('registroContrasena').value;
    const direccion = document.getElementById('registroDireccion').value;
    const ciudad = document.getElementById('registroCiudad').value;
    const ruc = document.getElementById('registroRuc').value;
    const telefono = document.getElementById('registroTelefono').value;

    console.log("Nombres: "+nombres);
    console.log("Apellidos: "+apellidos);
    console.log("Correo: "+correo);
    console.log("Contrasena: "+contrasena);
    console.log("Direccion: "+direccion);
    console.log("Ciudad: "+ciudad);
    console.log("Ruc: "+ruc);
    console.log("Telefono: "+telefono);


    console.log('REGISTRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');

    registrarBackend(nombres, apellidos, correo, contrasena, direccion, ciudad, ruc, telefono, function(response){
        if (response && response.success){
            data_log = response.data_usuario;
            quitarAccesos();
            mostrarMensajeBienvenida(data_log.Nombres+" "+data_log.Apellidos);
            alert('Registro de usuario correto !');
        }
        else{
            //mostrarFormularioRegistro() 
            alert(response.message);
        }
    });
}
function registrarBackend(nombres, apellidos, correo, contrasena, direccion, ciudad, ruc, telefono, callback) {
    fetch('/api/registro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombres, apellidos, correo, contrasena, direccion, ciudad, ruc, telefono })
    })
    .then(response => response.json())
    .then(data => {
        callback(data);
    })
    .catch(error => {
        console.error('Error:', error);
        callback({ success: false, message: 'Error en la solicitud al servidor' });
    });
}
//------------------------------------------------------------------------------------------------
function iniciarSesion(){
    const correo = document.getElementById('loginCorreo').value;
    const contrasena = document.getElementById('loginContrasena').value;
    iniciarSesionBackend(correo, contrasena, function(response){
        if (response && response.success){
            data_log = response.data_usuario;
            quitarAccesos();
            mostrarMensajeBienvenida(data_log.Nombres+" "+data_log.Apellidos);
            alert('Inicio de sesión correcta !');
        }
        else{
            //mostrarFormularioLogin() 
            alert(response.message);
        }
    });
}
function iniciarSesionBackend(correo, contrasena, callback) {
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correo, contrasena })
    })
    .then(response => response.json())
    .then(data => {
        callback(data);
    })
    .catch(error => {
        console.error('Error:', error);
        callback({ success: false, message: 'Error en la solicitud al servidor' });
    });
}
//------------------------------------------------------------------------------------------------










//Variable que mantiene el estado visible del carrito
var carritoVisible = false;

//Espermos que todos los elementos de la pàgina cargen para ejecutar el script
if(document.readyState == 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
}else{
    ready();
}

function ready(){
    
    //Agregremos funcionalidad a los botones eliminar del carrito
    var botonesEliminarItem = document.getElementsByClassName('btn-eliminar');
    for(var i=0;i<botonesEliminarItem.length; i++){
        var button = botonesEliminarItem[i];
        button.addEventListener('click',eliminarItemCarrito);
    }

    //Agrego funcionalidad al boton sumar cantidad
    var botonesSumarCantidad = document.getElementsByClassName('sumar-cantidad');
    for(var i=0;i<botonesSumarCantidad.length; i++){
        var button = botonesSumarCantidad[i];
        button.addEventListener('click',sumarCantidad);
    }

     //Agrego funcionalidad al buton restar cantidad
    var botonesRestarCantidad = document.getElementsByClassName('restar-cantidad');
    for(var i=0;i<botonesRestarCantidad.length; i++){
        var button = botonesRestarCantidad[i];
        button.addEventListener('click',restarCantidad);
    }

    //Agregamos funcionalidad al boton Agregar al carrito
    var botonesAgregarAlCarrito = document.getElementsByClassName('boton-item');
    for(var i=0; i<botonesAgregarAlCarrito.length;i++){
        var button = botonesAgregarAlCarrito[i];
        button.addEventListener('click', agregarAlCarritoClicked);
    }

    //Agregamos funcionalidad al botón comprar
    document.getElementsByClassName('btn-pagar')[0].addEventListener('click',pagarClicked)
}
//Eliminamos todos los elementos del carrito y lo ocultamos
function pagarClicked(){
    var itemsCarrito = document.querySelectorAll('.carrito-item');
    var itemsSeleccionados = [];

    
    if (data_log != null) {
        agregarEventListeners()

        itemsCarrito.forEach(item => {
            var id = item.querySelector('.carrito-item-id').innerText;
            var titulo = item.querySelector('.carrito-item-titulo').innerText;
            var cantidad = item.querySelector('.carrito-item-cantidad').value;

            itemsSeleccionados.push([id, titulo, cantidad]);
        });

        //mensaje = [itemsSeleccionados,data_log]

        mensaje = itemsSeleccionados;

        enviarAlBackend(mensaje, function(response) {
            if (response && response.success) {
                var resultadoFinal = response.resultado_final;

                alert("Gracias por la compra!\nDatos de su compra: "+ resultadoFinal);
                var carritoItems = document.getElementsByClassName('carrito-items')[0];
                while (carritoItems.hasChildNodes()) {
                    carritoItems.removeChild(carritoItems.firstChild);
                }
                actualizarTotalCarrito();
                ocultarCarrito();
            } else {
                alert(response.message);
            }
        });
    } else {
        alert('Debe iniciar sesión antes de proceder con la compra !');
    }
    
}

function enviarAlBackend(mensaje, callback) {
    fetch('/api/pagar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(mensaje)
    })
    .then(response => response.json())
    .then(data => {
        callback(data);
    })
    .catch(error => {
        console.error('Error:', error);
        callback({ success: false, message: 'Error en la solicitud al servidor' });
    });
}

//Funciòn que controla el boton clickeado de agregar al carrito
function agregarAlCarritoClicked(event){
    var button = event.target;
    var item = button.parentElement;
    var id = item.getElementsByClassName('id-item')[0].innerText
    var titulo = item.getElementsByClassName('titulo-item')[0].innerText;
    var precio = item.getElementsByClassName('precio-item')[0].innerText;
    var imagenSrc = item.getElementsByClassName('img-item')[0].src;
    console.log(imagenSrc);

    agregarItemAlCarrito(id, titulo, precio, imagenSrc);

    hacerVisibleCarrito();
}

//Funcion que hace visible el carrito
function hacerVisibleCarrito(){
    carritoVisible = true;
    var carrito = document.getElementsByClassName('carrito')[0];
    carrito.style.marginRight = '0';
    carrito.style.opacity = '1';

    var items =document.getElementsByClassName('contenedor-items')[0];
    items.style.width = '60%';
}

//Funciòn que agrega un item al carrito
function agregarItemAlCarrito(id, titulo, precio, imagenSrc){
    var item = document.createElement('div');
    item.classList.add = ('item');
    var itemsCarrito = document.getElementsByClassName('carrito-items')[0];

    //controlamos que el item que intenta ingresar no se encuentre en el carrito
    var nombresItemsCarrito = itemsCarrito.getElementsByClassName('carrito-item-titulo');
    for(var i=0;i < nombresItemsCarrito.length;i++){
        if(nombresItemsCarrito[i].innerText==titulo){
            alert("El item ya se encuentra en el carrito");
            return;
        }
    }

    var itemCarritoContenido = `
        <div class="carrito-item">
            <img src="${imagenSrc}" width="80px" alt="">
            <div class="carrito-item-detalles">
                <span class="carrito-item-id">${id}</span>
                <span class="carrito-item-titulo">${titulo}</span>
                <div class="selector-cantidad">
                    <i class="fa-solid fa-minus restar-cantidad"></i>
                    <input type="text" value="1" class="carrito-item-cantidad" disabled>
                    <i class="fa-solid fa-plus sumar-cantidad"></i>
                </div>
                <span class="carrito-item-precio">${precio}</span>
            </div>
            <button class="btn-eliminar">
                <i class="fa-solid fa-trash"></i>
            </button>
        </div>
    `
    item.innerHTML = itemCarritoContenido;
    itemsCarrito.append(item);

    //Agregamos la funcionalidad eliminar al nuevo item
     item.getElementsByClassName('btn-eliminar')[0].addEventListener('click', eliminarItemCarrito);

    //Agregmos al funcionalidad restar cantidad del nuevo item
    var botonRestarCantidad = item.getElementsByClassName('restar-cantidad')[0];
    botonRestarCantidad.addEventListener('click',restarCantidad);

    //Agregamos la funcionalidad sumar cantidad del nuevo item
    var botonSumarCantidad = item.getElementsByClassName('sumar-cantidad')[0];
    botonSumarCantidad.addEventListener('click',sumarCantidad);

    //Actualizamos total
    actualizarTotalCarrito();
}
//Aumento en uno la cantidad del elemento seleccionado
function sumarCantidad(event){
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    console.log(selector.getElementsByClassName('carrito-item-cantidad')[0].value);
    var cantidadActual = selector.getElementsByClassName('carrito-item-cantidad')[0].value;
    cantidadActual++;
    selector.getElementsByClassName('carrito-item-cantidad')[0].value = cantidadActual;
    actualizarTotalCarrito();
}
//Resto en uno la cantidad del elemento seleccionado
function restarCantidad(event){
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    console.log(selector.getElementsByClassName('carrito-item-cantidad')[0].value);
    var cantidadActual = selector.getElementsByClassName('carrito-item-cantidad')[0].value;
    cantidadActual--;
    if(cantidadActual>=1){
        selector.getElementsByClassName('carrito-item-cantidad')[0].value = cantidadActual;
        actualizarTotalCarrito();
    }
}

//Elimino el item seleccionado del carrito
function eliminarItemCarrito(event){
    var buttonClicked = event.target;
    buttonClicked.parentElement.parentElement.remove();
    //Actualizamos el total del carrito
    actualizarTotalCarrito();

    //la siguiente funciòn controla si hay elementos en el carrito
    //Si no hay elimino el carrito
    ocultarCarrito();
}
//Funciòn que controla si hay elementos en el carrito. Si no hay oculto el carrito.
function ocultarCarrito(){
    var carritoItems = document.getElementsByClassName('carrito-items')[0];
    if(carritoItems.childElementCount==0){
        var carrito = document.getElementsByClassName('carrito')[0];
        carrito.style.marginRight = '-100%';
        carrito.style.opacity = '0';
        carritoVisible = false;
    
        var items =document.getElementsByClassName('contenedor-items')[0];
        items.style.width = '100%';
    }
}

//Actualizamos el total de Carrito
function actualizarTotalCarrito(){
    var carritoItems = document.getElementsByClassName('carrito-item');
    var total = 0;

    for(var i = 0; i < carritoItems.length; i++){
        var item = carritoItems[i];
        var precioElemento = item.querySelector('.carrito-item-precio');
        var precioTexto = precioElemento.innerText.replace('S/ ', ''); // Asegúrate de tener solo el número
        var precio = parseFloat(precioTexto);

        var cantidadElemento = item.querySelector('.carrito-item-cantidad');
        var cantidad = parseInt(cantidadElemento.value);

        total += precio * cantidad;
    }

    total = Math.round(total * 100) / 100;

    var totalCarritoElemento = document.querySelector('.carrito-precio-total');
    totalCarritoElemento.innerText = 'S/ ' + total.toLocaleString('es-PE');
}