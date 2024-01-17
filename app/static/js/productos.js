let mostrador = document.getElementById("mostrador");
let seleccion = document.getElementById("seleccion");
let imgSeleccionada = document.getElementById("img");
let modeloSeleccionado = document.getElementById("modelo");
let precioSeleccionado = document.getElementById("precio");
let cantidadInput = document.getElementById("cantidad");
let agregarCarritoBtn = document.getElementById("agregar-carrito");

function cargar(item) {
    quitarBordes();
    mostrador.style.width = "60%";
    seleccion.style.width = "40%";
    seleccion.style.opacity = "1";
    item.style.border = "2px solid red";

    imgSeleccionada.src = item.getElementsByTagName("img")[0].src;
    modeloSeleccionado.innerHTML = item.getElementsByTagName("p")[0].innerHTML;
    precioSeleccionado.innerHTML = item.getElementsByTagName("span")[0].innerHTML;

    let productoId = item.dataset.productoId;
    cantidadInput.setAttribute('data-producto-id', productoId);
    cantidadInput.value = 1;
    agregarCarritoBtn.disabled = false;
}

function cerrar() {
    mostrador.style.width = "100%";
    seleccion.style.width = "0%";
    seleccion.style.opacity = "0";
    quitarBordes();
}

function quitarBordes() {
    var items = document.getElementsByClassName("item");
    for (i = 0; i < items.length; i++) {
        items[i].style.border = "none";
    }
}

function agregarAlCarrito() {
    var cantidad = $('#cantidad').val();

    $.ajax({
        type: 'POST',
        url: '/agregar-al-carrito/16',
        contentType: 'application/json',
        data: JSON.stringify({ cantidad: cantidad }),
        success: function(response) {
            console.log('Respuesta del Servidor:', response.message);
            alert(response.message);
            console.log('Producto agregado:', response.producto);
            // Actualizar la interfaz de usuario según tus necesidades
        },
        error: function(xhr, status, error) {
            console.error('Error en la solicitud AJAX:', status, error);
            console.log(xhr.responseText);
        }
    });
}
