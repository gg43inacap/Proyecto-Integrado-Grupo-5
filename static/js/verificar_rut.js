// --- Funciones de formateo y validación de RUT (adaptadas de login.js) ---
function formatearRut(valor) {
    let rutLimpio = valor.replace(/[^0-9kK]/g, '').toLowerCase();
    if (rutLimpio.length < 2) return rutLimpio;
    const dv = rutLimpio.slice(-1);
    const cuerpo = rutLimpio.slice(0, -1);
    let cuerpoFormateado = '';
    const cuerpoRevertido = cuerpo.split('').reverse().join('');
    for (let i = 0; i < cuerpoRevertido.length; i++) {
        if (i > 0 && i % 3 === 0) {
            cuerpoFormateado = '.' + cuerpoFormateado;
        }
        cuerpoFormateado = cuerpoRevertido[i] + cuerpoFormateado;
    }
    return cuerpoFormateado + '-' + dv;
}

function validarRut(valor) {
    if (!valor || valor.trim().length < 3) return false;
    if (!/^[0-9]{1,3}(\.[0-9]{3})*-?[0-9kK]$/.test(valor)) return false;
    // Validación de dígito verificador (algoritmo oficial)
    let rut = valor.replace(/\./g, '').replace(/-/g, '').toLowerCase();
    let cuerpo = rut.slice(0, -1);
    let dv = rut.slice(-1);
    let suma = 0, factor = 2;
    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += parseInt(cuerpo[i]) * factor;
        factor = factor === 7 ? 2 : factor + 1;
    }
    let dvEsperado = 11 - (suma % 11);
    dvEsperado = dvEsperado === 11 ? '0' : dvEsperado === 10 ? 'k' : dvEsperado.toString();
    return dv === dvEsperado;
}
// JS para verificar RUT de madre y redirigir según resultado

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-verificar-rut');
    const rutInput = document.getElementById('rut');
    const resultDiv = document.getElementById('rut-result');

    // Formatear automáticamente el RUT mientras se escribe
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

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const rut = rutInput.value.trim();
        if (!rut || !validarRut(rut)) {
            rutInput.classList.add('is-invalid');
            resultDiv.innerHTML = '<div class="alert alert-danger">Ingrese un RUT válido y bien formateado (con puntos y guion).</div>';
            return;
        }
        rutInput.classList.remove('is-invalid');
        resultDiv.innerHTML = '<div class="text-info">Buscando datos...</div>';
        fetch(`/gestion_some/api/madre_por_rut/?rut=${encodeURIComponent(rut)}`)
            .then(res => res.json())
            .then(data => {
                if (data.found) {
                    resultDiv.innerHTML = `<div class='alert alert-success'>\
                        <strong>Madre encontrada:</strong> ${data.nombre} <br>\
                        <button class='btn btn-success mt-3' id='btn-editar'>Editar datos</button>\
                    </div>`;
                    document.getElementById('btn-editar').onclick = function() {
                        window.location.href = `/gestion_some/madres/${data.id}/editar/`;
                    };
                } else {
                    resultDiv.innerHTML = `<div class='alert alert-warning'>\
                        No existe una madre registrada con este RUT.<br>\
                        <button class='btn btn-primary mt-3' id='btn-crear'>Registrar nueva madre</button>\
                    </div>`;
                    document.getElementById('btn-crear').onclick = function() {
                        window.location.href = `/gestion_some/madres/crear/?rut=${encodeURIComponent(rut)}`;
                    };
                }
            })
            .catch(() => {
                resultDiv.innerHTML = '<div class="alert alert-danger">Error al consultar el RUT. Intente nuevamente.</div>';
            });
    });
});
