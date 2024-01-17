document.addEventListener('DOMContentLoaded', function () {
    var alertContainer = document.getElementById('alert-container');

    if (alertContainer) {
        setTimeout(function () {
            alertContainer.style.opacity = '0';
            setTimeout(function () {
                alertContainer.parentNode.removeChild(alertContainer);
            }, 1000);  // 1000ms para esperar que se complete la transición de opacidad
        }, 3000);  // Desaparece después de 3 segundos
    }

});


