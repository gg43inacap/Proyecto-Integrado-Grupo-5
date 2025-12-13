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
});