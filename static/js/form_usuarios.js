// Validación y formateo de RUT
document.addEventListener('DOMContentLoaded', function() {
    const rutInput = document.getElementById('id_rut');
    
    function validarRut(rut) {
        const rutRegex = /^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$/;
        return rutRegex.test(rut);
    }
    
    function formatearRut(value) {
        // Limpiar y formatear RUT
        value = value.replace(/[^0-9kK]/g, '');
        
        if (value.length > 1) {
            const body = value.slice(0, -1);
            const dv = value.slice(-1).toUpperCase();
            
            let formatted = '';
            for (let i = body.length - 1, j = 1; i >= 0; i--, j++) {
                formatted = body.charAt(i) + formatted;
                if (j % 3 === 0 && i !== 0) {
                    formatted = '.' + formatted;
                }
            }
            return formatted + '-' + dv;
        }
        return value;
    }
    
    if (rutInput) {
        rutInput.addEventListener('input', function(e) {
            const formatted = formatearRut(e.target.value);
            e.target.value = formatted;
            
            if (formatted && !validarRut(formatted)) {
                e.target.setCustomValidity('Formato de RUT inválido. Ejemplo: 12.345.678-9');
                e.target.classList.add('is-invalid');
            } else {
                e.target.setCustomValidity('');
                e.target.classList.remove('is-invalid');
            }
        });
    }
});