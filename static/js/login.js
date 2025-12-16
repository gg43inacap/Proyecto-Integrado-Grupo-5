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
    let usernameListener = null;

    function formatearRut(valor) {
        // Limpiar el valor de entrada (solo números y K)
        let rutLimpio = valor.replace(/[^0-9kK]/g, '').toUpperCase();
        
        // Limitar a máximo 9 caracteres
        if (rutLimpio.length > 9) {
            rutLimpio = rutLimpio.substring(0, 9);
        }
        
        // Si tiene menos de 2 caracteres, no formatear
        if (rutLimpio.length < 2) {
            return rutLimpio;
        }
        
        // Separar cuerpo y dígito verificador
        const dv = rutLimpio.slice(-1);
        const cuerpo = rutLimpio.slice(0, -1);
        
        // Formatear el cuerpo con puntos
        let cuerpoFormateado = '';
        const cuerpoRevertido = cuerpo.split('').reverse().join('');
        
        for (let i = 0; i < cuerpoRevertido.length; i++) {
            if (i > 0 && i % 3 === 0) {
                cuerpoFormateado = '.' + cuerpoFormateado;
            }
            cuerpoFormateado = cuerpoRevertido[i] + cuerpoFormateado;
        }
        
        // Retornar formato completo
        return cuerpoFormateado + '-' + dv;
    }
    
    function validarRut(valor) {
        // Validación básica para mostrar feedback visual
        if (!valor || valor.trim().length < 3) return false;
        
        // Verificar que termine con guión y dígito verificador
        if (!/.*-[0-9kK]$/.test(valor)) return false;
        
        return true;
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
            const cursorPos = userInput.selectionStart;
            const valorAntes = userInput.value;
            
            // Formatear automáticamente mientras el usuario escribe
            const valorFormateado = formatearRut(userInput.value);
            
            // Solo actualizar si el valor cambió
            if (valorFormateado !== valorAntes) {
                userInput.value = valorFormateado;
                
                // Ajustar posición del cursor
                let nuevaPos = cursorPos;
                if (valorFormateado.length > valorAntes.length && (valorFormateado[cursorPos-1] === '.' || valorFormateado[cursorPos-1] === '-')) {
                    nuevaPos = cursorPos + 1;
                }
                userInput.setSelectionRange(nuevaPos, nuevaPos);
            }
            
            // Mostrar indicación visual
            if (userInput.value.trim()) {
                if (!validarRut(userInput.value)) {
                    userInput.classList.add('is-invalid');
                } else {
                    userInput.classList.remove('is-invalid');
                }
            } else {
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

    function addUsernameFormatting() {
        if (!userInput) return;

        // Remover cualquier listener anterior
        removeUsernameFormatting();
        
        usernameListener = function() {
            const cursorPos = userInput.selectionStart;
            const valorAntes = userInput.value;
            const valorLowercase = userInput.value.toLowerCase();
            
            if (valorLowercase !== valorAntes) {
                userInput.value = valorLowercase;
                userInput.setSelectionRange(cursorPos, cursorPos);
            }
        };
        userInput.addEventListener('input', usernameListener);
    }

    function removeUsernameFormatting() {
        if (userInput && usernameListener) {
            userInput.removeEventListener('input', usernameListener);
            usernameListener = null;
        }
    }

    function updateField() {
        if (!userInput || !userLabel || !userHelp || !rutRadio) return;

        // Autowipe: limpiar el campo al cambiar método
        userInput.value = '';
        
        if (rutRadio.checked) {
            userLabel.textContent = 'RUT';
            userInput.placeholder = 'Ej: 123456789 (se formateará automáticamente)';
            userHelp.textContent = 'Escriba solo números y K - se formatearán automáticamente con puntos y guión';
            userInput.setAttribute('maxlength', '12');
            removeUsernameFormatting();
            addRutValidation();
        } else {
            userLabel.textContent = 'Cuenta de usuario';
            userInput.placeholder = 'Ingrese su cuenta de usuario (en minúsculas)';
            userHelp.textContent = 'Ingrese su cuenta de usuario (se convertirá a minúsculas automáticamente)';
            userInput.removeAttribute('maxlength');
            removeRutValidation();
            addUsernameFormatting();
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