const container = document.getElementById('container');
        const registerBtn = document.getElementById('register');
        const loginBtn = document.getElementById('login');

        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });

        loginBtn.addEventListener('click', () => {
            container.classList.remove("active");
        });


        


document.addEventListener('DOMContentLoaded', function () {
    var errorAlert = document.getElementById('login-error-alert');
    var errorMessage = "{{ error_message }}";

    if (errorMessage) {
        // Crea un elemento div para la notificación flotante
        var notificationContainer = document.getElementById('notification-container');
        var notification = document.createElement('div');
        notification.classList.add('notification');
        notification.textContent = errorMessage;

        // Agrega la notificación al contenedor
        notificationContainer.appendChild(notification);

        // Muestra la notificación
        setTimeout(function () {
            notification.classList.add('show');
        }, 100);

        // Desaparece después de 3 segundos
        setTimeout(function () {
            notification.classList.remove('show');
            setTimeout(function () {
                // Elimina la notificación después de la transición de salida
                notificationContainer.removeChild(notification);
            }, 1000);
        }, 3000);
    }
});


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

function togglePasswordVisibility(passwordId) {
    var passwordInput = document.getElementById(passwordId);
    var toggleIcon = document.querySelector(`#${passwordId} + .toggle-password i`);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    } else {
        passwordInput.type = "password";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    }
}


