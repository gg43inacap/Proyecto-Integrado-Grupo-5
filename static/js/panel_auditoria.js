document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
    cargarUltimosEventos();
});

function cargarEstadisticas() {
    // Simulación de carga de estadísticas (en un entorno real, esto sería una llamada AJAX)
    fetch('{% url "lista_auditorias" %}')
    .then(response => {
        // Actualizar contadores (esto se haría con una API real)
        document.getElementById('total-eventos').textContent = 'Calculando...';
        document.getElementById('eventos-hoy').textContent = 'Calculando...';
        document.getElementById('eventos-semana').textContent = 'Calculando...';
        
        // Simular valores (en implementación real, vendría del servidor)
        setTimeout(() => {
            document.getElementById('total-eventos').textContent = Math.floor(Math.random() * 1000) + 100;
            document.getElementById('eventos-hoy').textContent = Math.floor(Math.random() * 50) + 10;
            document.getElementById('eventos-semana').textContent = Math.floor(Math.random() * 300) + 50;
        }, 1000);
    })
    .catch(error => {
        console.log('Error cargando estadísticas:', error);
        document.getElementById('total-eventos').textContent = 'Error';
        document.getElementById('eventos-hoy').textContent = 'Error';
        document.getElementById('eventos-semana').textContent = 'Error';
    });
}

function cargarUltimosEventos() {
    // En un entorno real, esto cargaría los últimos eventos vía AJAX
    setTimeout(() => {
        document.getElementById('ultimos-eventos').innerHTML = `
            <div class="text-center">
                <p class="text-muted">Últimos eventos del sistema aparecerán aquí</p>
                <a href="{% url 'lista_auditorias' %}" class="btn btn-primary">
                    <i class="fas fa-list"></i> Ver Lista Completa de Eventos
                </a>
            </div>
        `;
    }, 2000);
}