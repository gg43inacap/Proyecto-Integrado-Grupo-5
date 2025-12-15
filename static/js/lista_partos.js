document.addEventListener('DOMContentLoaded', function() {
    // Lógica para el botón 'Completar' (Requiere confirmación)
    document.querySelectorAll('.btn-complete-parto').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            const url = this.dataset.url;
            
            if (url) {
                if (confirm('¿Desea marcar este parto como completado? Esta acción es irreversible.')) {
                    // Redirigir a la URL de completado
                    window.location.href = url;
                }
            }
        });
    });
});