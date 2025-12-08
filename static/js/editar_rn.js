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
});