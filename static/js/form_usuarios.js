// Validación y formateo de RUT y formateo de nombre de usuario (minúsculas)
document.addEventListener('DOMContentLoaded', function() {
    const rutInput = document.getElementById('id_rut');
    const usernameInput = document.getElementById('id_username');

    function validarRut(rut) {
        // Formato esperado: 12.345.678-9 o 1.234.567-8
        const rutRegex = /^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$/;
        return rutRegex.test(rut);
    }

    function formatearRut(value) {
        // Limpiar: dejar solo números y K/k
        let clean = value.replace(/[^0-9kK]/g, '').toUpperCase();

        if (clean.length <= 1) return clean;

        const dv = clean.slice(-1);
        let body = clean.slice(0, -1);

        // Limitar longitud razonable
        if (body.length > 8) body = body.slice(0, 8);

        // Insertar puntos cada 3 dígitos desde la derecha
        let formattedBody = '';
        for (let i = body.length - 1, j = 0; i >= 0; i--, j++) {
            formattedBody = body.charAt(i) + formattedBody;
            if ((j + 1) % 3 === 0 && i !== 0) formattedBody = '.' + formattedBody;
        }

        return formattedBody + '-' + dv;
    }

    // Formateo y validación en tiempo real para el campo RUT
    if (rutInput) {
        rutInput.addEventListener('input', function(e) {
            const cursor = rutInput.selectionStart;
            const before = rutInput.value;
            const formatted = formatearRut(before);

            if (formatted !== before) {
                rutInput.value = formatted;
                // tratar de mantener la posición del cursor
                try { rutInput.setSelectionRange(cursor, cursor); } catch (err) { /* ignore */ }
            }

            if (formatted && !validarRut(formatted)) {
                rutInput.setCustomValidity('Formato de RUT inválido. Ejemplo: 12.345.678-9');
                rutInput.classList.add('is-invalid');
            } else {
                rutInput.setCustomValidity('');
                rutInput.classList.remove('is-invalid');
            }
        });

        // validación final en blur
        rutInput.addEventListener('blur', function() {
            if (rutInput.value && !validarRut(rutInput.value)) {
                rutInput.classList.add('is-invalid');
            } else {
                rutInput.classList.remove('is-invalid');
            }
        });
    }

    // Formateo automático a minúsculas para el nombre de usuario
    if (usernameInput) {
        usernameInput.addEventListener('input', function(e) {
            const pos = usernameInput.selectionStart;
            const before = usernameInput.value;
            const lowered = before.toLowerCase();

            if (lowered !== before) {
                usernameInput.value = lowered;
                try { usernameInput.setSelectionRange(pos, pos); } catch (err) { /* ignore */ }
            }
        });

        // Opcional: prevenir espacios al inicio/final y validar mínima longitud
        usernameInput.addEventListener('blur', function() {
            if (!usernameInput.value) return;
            usernameInput.value = usernameInput.value.trim();
            if (usernameInput.value.length < 3) {
                usernameInput.setCustomValidity('El nombre de usuario debe tener al menos 3 caracteres.');
                usernameInput.classList.add('is-invalid');
            } else {
                usernameInput.setCustomValidity('');
                usernameInput.classList.remove('is-invalid');
            }
        });
    }

    // Validación de contraseña segura con checklist en tiempo real
    const passwordInput = document.getElementById('id_password');
    if (passwordInput) {
        // Crear el checklist de requisitos
        const passwordChecklistHTML = `
            <div class="password-strength-container mt-2">
                <div class="password-strength-label mb-2">
                    <small class="text-muted"><i class="fas fa-shield-alt"></i> Requisitos de contraseña segura:</small>
                </div>
                <div class="password-checklist">
                    <div class="checklist-item" data-requirement="length">
                        <i class="fas fa-circle check-icon"></i>
                        <span class="check-text">Mínimo 8 caracteres</span>
                    </div>
                    <div class="checklist-item" data-requirement="uppercase">
                        <i class="fas fa-circle check-icon"></i>
                        <span class="check-text">Contiene mayúscula (A-Z)</span>
                    </div>
                    <div class="checklist-item" data-requirement="lowercase">
                        <i class="fas fa-circle check-icon"></i>
                        <span class="check-text">Contiene minúscula (a-z)</span>
                    </div>
                    <div class="checklist-item" data-requirement="number">
                        <i class="fas fa-circle check-icon"></i>
                        <span class="check-text">Contiene número (0-9)</span>
                    </div>
                    <div class="checklist-item" data-requirement="special">
                        <i class="fas fa-circle check-icon"></i>
                        <span class="check-text">Contiene carácter especial (!@#$%^&*)</span>
                    </div>
                </div>
                <div class="password-strength-meter mt-2">
                    <div class="strength-bar">
                        <div class="strength-fill" style="width: 0%"></div>
                    </div>
                    <div class="strength-text text-muted" style="font-size: 0.85rem; margin-top: 0.25rem;">
                        Fortaleza: <span class="strength-label">Muy débil</span>
                    </div>
                </div>
            </div>
        `;

        // Insertar el checklist después del campo de contraseña
        passwordInput.insertAdjacentHTML('afterend', passwordChecklistHTML);

        // Función para validar contraseña
        function validatePassword(password) {
            const requirements = {
                length: password.length >= 8,
                uppercase: /[A-Z]/.test(password),
                lowercase: /[a-z]/.test(password),
                number: /\d/.test(password),
                special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
            };

            return requirements;
        }

        // Función para actualizar el checklist visual
        function updatePasswordChecklist() {
            const password = passwordInput.value;
            const requirements = validatePassword(password);
            
            // Actualizar cada item del checklist
            Object.keys(requirements).forEach(req => {
                const item = document.querySelector(`.checklist-item[data-requirement="${req}"]`);
                const icon = item.querySelector('.check-icon');
                
                if (requirements[req]) {
                    item.classList.add('checked');
                    icon.classList.remove('fa-circle');
                    icon.classList.add('fa-check-circle');
                    icon.style.color = '#10b981';
                } else {
                    item.classList.remove('checked');
                    icon.classList.remove('fa-check-circle');
                    icon.classList.add('fa-circle');
                    icon.style.color = '#d1d5db';
                }
            });

            // Calcular fortaleza de contraseña
            const metCriteria = Object.values(requirements).filter(v => v).length;
            const strengthPercent = (metCriteria / 5) * 100;
            
            // Actualizar la barra de fortaleza
            const strengthFill = document.querySelector('.strength-fill');
            const strengthLabel = document.querySelector('.strength-label');
            
            strengthFill.style.width = strengthPercent + '%';
            
            if (metCriteria === 0) {
                strengthFill.style.backgroundColor = '#d1d5db';
                strengthLabel.textContent = 'Muy débil';
            } else if (metCriteria <= 2) {
                strengthFill.style.backgroundColor = '#ef4444';
                strengthLabel.textContent = 'Débil';
            } else if (metCriteria === 3) {
                strengthFill.style.backgroundColor = '#f59e0b';
                strengthLabel.textContent = 'Media';
            } else if (metCriteria === 4) {
                strengthFill.style.backgroundColor = '#3b82f6';
                strengthLabel.textContent = 'Fuerte';
            } else {
                strengthFill.style.backgroundColor = '#10b981';
                strengthLabel.textContent = 'Muy fuerte';
            }

            // Validación del formulario
            const allMet = Object.values(requirements).every(v => v);
            if (password && !allMet) {
                passwordInput.setCustomValidity('La contraseña no cumple con todos los requisitos de seguridad.');
                passwordInput.classList.add('is-invalid');
            } else {
                passwordInput.setCustomValidity('');
                passwordInput.classList.remove('is-invalid');
            }
        }

        // Escuchar cambios en el campo de contraseña
        passwordInput.addEventListener('input', updatePasswordChecklist);
        passwordInput.addEventListener('focus', function() {
            document.querySelector('.password-strength-container').style.display = 'block';
        });
    }
});