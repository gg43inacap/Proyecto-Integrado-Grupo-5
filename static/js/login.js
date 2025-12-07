document.addEventListener('DOMContentLoaded', function() {
    // Alternar visibilidad de contraseña
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
    });
    
    // Formatear RUT mientras se escribe SOLO si método RUT está seleccionado
    const usernameInput = document.getElementById('username');
    const rutRadio = document.getElementById('login_rut');
    const usernameRadio = document.getElementById('login_username');
    
    // Autowipe: limpiar campo al cambiar método de login
    if (rutRadio) {
        rutRadio.addEventListener('change', function() {
            if (this.checked) {
                usernameInput.value = '';
            }
        });
    }
    
    if (usernameRadio) {
        usernameRadio.addEventListener('change', function() {
            if (this.checked) {
                usernameInput.value = '';
            }
        });
    }
    
    usernameInput.addEventListener('input', function(e) {
        // Solo formatear si el método RUT está seleccionado
        if (rutRadio && rutRadio.checked) {
            let value = e.target.value.replace(/[^0-9kK]/g, '');
            
            if (value.length > 0) {
                // Formatear con puntos y guión
                let formatted = '';
                const body = value.slice(0, -1);
                const dv = value.slice(-1).toUpperCase();
                
                // Agregar puntos
                for (let i = body.length - 1, j = 1; i >= 0; i--, j++) {
                    formatted = body.charAt(i) + formatted;
                    if (j % 3 === 0 && i !== 0) {
                        formatted = '.' + formatted;
                    }
                }
                
                // Agregar guión y dígito verificador
                formatted = formatted + '-' + dv;
                e.target.value = formatted;
            }
        }
        // Si no es modo RUT, no formatear nada
    });
    
    // Validar formato de RUT antes de enviar
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        const username = usernameInput.value;
        
        // Validar formato de RUT SOLO si método RUT está seleccionado
        if (rutRadio && rutRadio.checked && !validateRUT(username)) {
            e.preventDefault();
            showAlert('Por favor ingrese un RUT válido (Ej: 12.345.678-9)', 'warning');
            usernameInput.focus();
            return false;
        }
        
        // Guardar en localStorage si "Recordar" está activado
        const rememberMe = document.getElementById('rememberMe');
        if (rememberMe.checked) {
            localStorage.setItem('neonatal_username', username);
        } else {
            localStorage.removeItem('neonatal_username');
        }
        
        return true;
    });
    
    // Cargar usuario guardado si existe
    const savedUsername = localStorage.getItem('neonatal_username');
    if (savedUsername) {
        usernameInput.value = savedUsername;
        document.getElementById('rememberMe').checked = true;
    }
    
    // Función para validar RUT
    function validateRUT(rut) {
        // Eliminar puntos y guión
        const cleanRut = rut.replace(/\./g, '').replace(/-/g, '').toUpperCase();
        
        // Validar formato básico
        if (!/^[0-9]+[0-9K]$/.test(cleanRut)) {
            return false;
        }
        
        // El RUT debe tener al menos 2 caracteres (número + dígito verificador)
        if (cleanRut.length < 2) {
            return false;
        }
        
        return true;
    }
    
    // Función para mostrar alertas
    function showAlert(message, type) {
        // Crear elemento de alerta
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas ${type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insertar después del título
        const title = document.querySelector('.login-body h2');
        if (title) {
            title.parentNode.insertBefore(alertDiv, title.nextSibling);
        }
        
        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 5000);
    }
    
    // Efecto de entrada para el formulario
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

    // Si hay mensajes de Django, mostrarlos como notificación
    const messagesElement = document.getElementById('django-messages');
    if (messagesElement) {
        // Asume que los mensajes están codificados como JSON en el atributo data
        const messagesData = JSON.parse(messagesElement.getAttribute('data-messages'));
        messagesData.forEach(msg => {
            showNotificationJS(msg.message, msg.tags);
        });
    }
});