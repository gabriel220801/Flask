document.addEventListener('DOMContentLoaded', function () {
    // Función para manejar clic en el botón "Eliminar"
    function eliminarProducto(event) {
        const productId = event.target.getAttribute('data-product-id');
    
        // Preguntar al usuario si desea eliminar el producto
        const confirmacion = confirm('¿Estás seguro de que deseas eliminar este producto del carrito?');
    
        if (confirmacion) {
            // Realizar la solicitud al servidor para eliminar el producto del carrito
            fetch(`/eliminar-del-carrito/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error al eliminar el producto del carrito. Código: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    // Actualizar la interfaz o realizar otras acciones según tu lógica
                    alert('Producto eliminado del carrito exitosamente');
                    window.location.reload(); // Recargar la página para reflejar los cambios en el carrito
                } else {
                    console.error('Error al eliminar el producto del carrito:', data.error);
                }
            })
            .catch(error => {
                console.error('Error de red:', error);
            });
        }
    }

    // Función para manejar clic en el botón "Realizar Compra"

// Función para manejar clic en el botón "Realizar Compra"
function realizarCompra(event) {
    event.preventDefault();

    // Obtener los productos seleccionados
    const productosSeleccionados = document.querySelectorAll('input[name="productos_seleccionados"]:checked');
    const productosNombres = [];
    let totalCompra = 0;

    productosSeleccionados.forEach((checkbox, index) => {
        const card = checkbox.closest('.card');
        const nombreProducto = card.querySelector('h4').innerText;
        const precioProducto = parseFloat(card.querySelector('p').innerText.replace('Precio: $', ''));
        const cantidadProducto = parseInt(card.querySelector('p:nth-child(3)').innerText.replace('Cantidad: ', ''), 10);

        totalCompra += precioProducto * cantidadProducto;

        productosNombres.push(`${index + 1}. ${nombreProducto} (Cantidad: ${cantidadProducto}) -> $${precioProducto * cantidadProducto}`);
    });

    // Mostrar un mensaje con los detalles de la compra y el total
    const mensaje = productosNombres.length > 0
        ? `Productos seleccionados:\n${productosNombres.join('\n')}\n\nTotal de la compra: $${totalCompra.toFixed(2)}`
        : 'No has seleccionado ningún producto para comprar';

    alert(mensaje);

    // Desmarcar los productos seleccionados
    productosSeleccionados.forEach(checkbox => {
        checkbox.checked = false;
    });

    // Realizar la solicitud al servidor para realizar la compra
    fetch('/realizar-compra', {
        method: 'POST',
        body: JSON.stringify({ productosIds }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        // ... (código posterior)
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
}

    // Agregar un escuchador de eventos a todos los botones "Eliminar"
    const eliminarBtns = document.querySelectorAll('.eliminar-btn');
    eliminarBtns.forEach(btn => {
        btn.addEventListener('click', eliminarProducto);
    });

    // Agregar un escuchador de eventos al botón "Realizar Compra"
    const realizarCompraBtn = document.querySelector('.realizar-compra-btn');
    realizarCompraBtn.addEventListener('click', realizarCompra);
});


