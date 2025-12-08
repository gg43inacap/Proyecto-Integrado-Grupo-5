document.addEventListener('DOMContentLoaded', function() {

    // ==========================================================
    // 1. Lógica de Alternancia de Contraseña
    // ==========================================================
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            // Toggle the icon
            this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
        });
    }

    // ==========================================================
    // 2. Lógica de Cambio y Validación de RUT/Usuario
    // (Script recién agregado)
    // ==========================================================
    const usernameRadio = document.getElementById('login_username');
    const rutRadio = document.getElementById('login_rut');
    const userLabel = document.getElementById('user-label');
    const userInput = document.getElementById('username');
    const userHelp = document.getElementById('user-help');
    let rutListener = null;

    function validarRut(valor) {
        // Regex para formato XX.XXX.XXX-X (simple, asumiendo que el guión ya existe)
        const rutRegex = /^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$/;
        return rutRegex.test(valor);
    }

    function limpiarRestricciones() {
        if (userInput) {
            userInput.setCustomValidity('');
            userInput.classList.remove('is-invalid');
        }
    }

    function addRutValidation() {
        if (!userInput) return;

        removeRutValidation(); // Asegura que no se dupliquen listeners
        rutListener = function() {
            // Solo validar si hay valor y el formato es incorrecto
            if (userInput.value && !validarRut(userInput.value)) {
                userInput.setCustomValidity('Formato de RUT inválido. Ejemplo: 12.345.678-9');
                userInput.classList.add('is-invalid');
            } else {
                userInput.setCustomValidity('');
                userInput.classList.remove('is-invalid');
            }
        };
        userInput.addEventListener('input', rutListener);
    }

    function removeRutValidation() {
        if (userInput && rutListener) {
            userInput.removeEventListener('input', rutListener);
            rutListener = null;
        }
        limpiarRestricciones();
    }

    function updateField() {
        if (!userInput || !userLabel || !userHelp || !rutRadio) return;

        // Autowipe: limpiar el campo al cambiar método
        userInput.value = '';
        
        if (rutRadio.checked) {
            userLabel.textContent = 'RUT';
            userInput.placeholder = 'Ej: 12.345.678-9';
            userHelp.textContent = 'Ingrese su RUT con puntos y guión';
            userInput.setAttribute('maxlength', '12'); // Limitar longitud para RUT
            addRutValidation();
        } else {
            userLabel.textContent = 'Cuenta de usuario';
            userInput.placeholder = 'Ingrese su cuenta de usuario';
            userHelp.textContent = 'Ingrese su cuenta de usuario';
            userInput.removeAttribute('maxlength'); // Quitar límite para nombre de usuario
            removeRutValidation();
        }
    }

    // Inicialización de la lógica RUT/Usuario
    if (usernameRadio && rutRadio) {
        usernameRadio.addEventListener('change', updateField);
        rutRadio.addEventListener('change', updateField);
        updateField(); // Llamar al inicio para establecer el estado inicial
    }

    // ==========================================================
    // 3. Lógica de Notificaciones (del código anterior)
    // ==========================================================

    // Función para mostrar notificaciones (mensajes de error/éxito)
    function showNotificationJS(message, type) {
        if (typeof bootstrap === 'undefined') {
            console.error("Bootstrap JS no está cargado. No se pueden mostrar notificaciones.");
            return;
        }

        const alertDiv = document.createElement('div');
        // Usamos la clase personalizada 'alert-custom-js' definida en style.css
        alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-custom-js`; 
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            <i class="fas ${type === 'warning' || type === 'error' ? 'fa-exclamation-triangle' : 'fa-info-circle'} me-2 alert-icon"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Insertar en un lugar visible (usando document.body.prepend para que flote)
        document.body.prepend(alertDiv);
        

        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                // Usar la API de Bootstrap para un cierre suave
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alertDiv);
                bsAlert.close();
            }
        }, 5000);
    }
    
    // Efecto de entrada para el formulario (del código anterior)
    const formGroups = document.querySelectorAll('.form-group-custom');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            group.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 100 + (index * 100));
    });

    // Si hay mensajes de Django, mostrarlos como notificación (del código anterior)
    const messagesElement = document.getElementById('django-messages');
    if (messagesElement) {
        try {
            const messagesData = JSON.parse(messagesElement.getAttribute('data-messages'));
            messagesData.forEach(msg => {
                // Mapear tags de Django a tipos de alerta de Bootstrap
                let alertType = msg.tags;
                if (alertType === 'error') alertType = 'danger'; 
                
                showNotificationJS(msg.message, alertType);
            });
        } catch (e) {
            console.error("Error al parsear mensajes de Django:", e);
        }
    }
});