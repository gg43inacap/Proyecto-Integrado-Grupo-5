// Función para limpiar filtros
function limpiarFiltros() {
    document.getElementById('accion').value = '';
    document.getElementById('modelo').value = '';
    document.getElementById('usuario').value = '';
    document.getElementById('fecha_desde').value = '';
    document.getElementById('orden').value = '-fecha_hora';
    document.getElementById('filtrosForm').submit();
}

// Opcional: Auto-submit cuando cambia el ordenamiento
document.addEventListener('DOMContentLoaded', function() {
    const ordenSelect = document.getElementById('orden');
    if (ordenSelect) {
        ordenSelect.addEventListener('change', function() {
            document.getElementById('filtrosForm').submit();
        });
    }
});