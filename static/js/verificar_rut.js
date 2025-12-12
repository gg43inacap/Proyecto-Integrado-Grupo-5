// JS para verificar RUT de madre y redirigir según resultado

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-verificar-rut');
    const rutInput = document.getElementById('rut');
    const resultDiv = document.getElementById('rut-result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const rut = rutInput.value.trim();
        if (!rut) return;
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
                        window.location.href = `/gestion_some/madres/${rut}/editar/`;
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
