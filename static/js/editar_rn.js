function filtrarPartos() {
    const madreSelect = document.getElementById('id_madre');
    const partoSelect = document.getElementById('id_parto_asociado');
    
    if (!madreSelect || !partoSelect) {
        console.log('No se encontraron los selects de madre o parto');
        return;
    }
    
    const madreId = madreSelect.value;
    console.log('Madre seleccionada ID:', madreId);
    
    // Limpiar opciones actuales del select de partos
    partoSelect.innerHTML = '<option value="">Cargando...</option>';
    
    if (madreId) {
        const url = `/partos/ajax/filtrar-partos/?madre_id=${madreId}`;
        console.log('URL petición:', url);
        
        fetch(url)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data);
                
                // Limpiar el select
                partoSelect.innerHTML = '<option value="">---------</option>';
                
                if (data.error) {
                    console.error('Error del servidor:', data.error);
                    const option = new Option(`Error: ${data.error}`, '');
                    option.disabled = true;
                    partoSelect.add(option);
                } else {
                    data.partos.forEach(parto => {
                        const option = new Option(parto.text, parto.id);
                        partoSelect.add(option);
                    });
                    
                    // Mostrar mensaje si no hay partos activos
                    if (data.partos.length === 0) {
                        const option = new Option('No hay partos activos para esta madre', '');
                        option.disabled = true;
                        partoSelect.add(option);
                    }
                }
            })
            .catch(error => {
                console.error('Error completo:', error);
                partoSelect.innerHTML = '<option value="">---------</option>';
                const option = new Option(`Error de conexión: ${error.message}`, '');
                option.disabled = true;
                partoSelect.add(option);
            });
    } else {
        partoSelect.innerHTML = '<option value="">---------</option>';
    }
}

// Configurar evento onchange y ejecutar filtrado inicial
document.addEventListener('DOMContentLoaded', function() {
    const madreSelect = document.getElementById('id_madre');
    if (madreSelect) {
        madreSelect.addEventListener('change', filtrarPartos);

        // Ejecutar filtrado inicial si hay una madre preseleccionada
        if (madreSelect.value) {
            filtrarPartos();
        }
    }

    // Configurar control de anomalía congénita
    const checkboxAnomalia = document.getElementById('id_anomalia_congenita');
    const inputDescripcion = document.getElementById('id_descripcion_anomalia');

    if (checkboxAnomalia && inputDescripcion) {
        const containerDescripcion = inputDescripcion.closest('.mb-3');

        function toggleDescripcionAnomalia() {
            if (checkboxAnomalia.checked) {
                if (containerDescripcion) containerDescripcion.style.display = 'block';
                inputDescripcion.required = true;
            } else {
                if (containerDescripcion) containerDescripcion.style.display = 'none';
                inputDescripcion.required = false;
                inputDescripcion.value = '';
            }
        }

        // Establecer estado inicial
        toggleDescripcionAnomalia();

        // Agregar evento change
        checkboxAnomalia.addEventListener('change', toggleDescripcionAnomalia);
    }

    // Aplicar formato automático a fecha y hora del formulario de edición
    const fechaInput = document.querySelector('input[name="fecha_nacimiento"]');
    if (fechaInput) {
        fechaInput.classList.add('calendario-amigable');
        if (!fechaInput.dataset.calendarioIniciado) {
            new CalendarioAmigable(fechaInput);
            fechaInput.dataset.calendarioIniciado = 'true';
        }
        fechaInput.addEventListener('input', function() { formatoFecha(this); });
        fechaInput.setAttribute('maxlength', '10');
    }

    const horaInput = document.querySelector('input[name="hora_nacimiento"]');
    if (horaInput) {
        horaInput.classList.add('horario-amigable');
        if (!horaInput.dataset.horarioIniciado) {
            new HorarioAmigable(horaInput);
            horaInput.dataset.horarioIniciado = 'true';
        }
        horaInput.addEventListener('input', function() { formatoHora(this); });
        horaInput.setAttribute('maxlength', '5');
    }
});
