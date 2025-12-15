// Este script se aplica a cualquier input con id="id_rut"
// Usa las funciones ya definidas en verificar_rut.js (formatearRut y validarRut)

document.addEventListener('DOMContentLoaded', function() {
    const rutInput = document.getElementById('id_rut');
    if (rutInput) {
        rutInput.addEventListener('input', function() {
            const valorAntes = rutInput.value;
            const valorFormateado = formatearRut(valorAntes);
            if (valorFormateado !== valorAntes) {
                rutInput.value = valorFormateado;
            }

            // Feedback visual
            if (rutInput.value.trim()) {
                if (!validarRut(rutInput.value)) {
                    rutInput.classList.add('is-invalid');
                } else {
                    rutInput.classList.remove('is-invalid');
                }
            } else {
                rutInput.classList.remove('is-invalid');
            }
        });
    }
});