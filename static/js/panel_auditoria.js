document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
    cargarUltimosEventos();
});

// Función para traducir acciones al español con emojis
function traducirAccion(accion) {
    const traducciones = {
        'CREATE': '📝 Creación',
        'UPDATE': '✏️ Modificación',
        'DELETE': '🗑️ Eliminación',
        'LOGIN_SUCCESS': '✅ Login Exitoso',
        'LOGIN_FAILED': '❌ Login Fallido',
        'LOGOUT': '🚪 Cierre Sesión',
        'VIEW': '👁️ Visualización',
        'USER_BLOCKED': '🚫 Usuario Bloqueado',
        'ACCESS_DENIED': '⛔ Acceso Denegado'
    };
    return traducciones[accion] || accion;
}

// Función para obtener el color del badge según la acción
function obtenerColorAccion(accion) {
    const colores = {
        'CREATE': 'success',
        'UPDATE': 'primary',
        'DELETE': 'danger',
        'LOGIN_SUCCESS': 'success',
        'LOGIN_FAILED': 'danger',
        'LOGOUT': 'warning',
        'VIEW': 'secondary',
        'USER_BLOCKED': 'danger',
        'ACCESS_DENIED': 'danger'
    };
    return colores[accion] || 'dark';
}

function cargarEstadisticas() {
    // Hacer fetch al API real de estadísticas
    fetch('/auditoria/api/estadisticas/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Actualizar contadores con datos REALES
        document.getElementById('total-eventos').textContent = data.total_eventos || 0;
        document.getElementById('eventos-hoy').textContent = data.eventos_hoy || 0;
        document.getElementById('eventos-semana').textContent = data.eventos_semana || 0;
        
        // Guardar datos para uso posterior (gráficas, etc)
        window.estadisticasAuditoria = data;
        
        console.log('Estadísticas cargadas correctamente:', data);
    })
    .catch(error => {
        console.error('Error cargando estadísticas:', error);
        document.getElementById('total-eventos').textContent = 'Error';
        document.getElementById('eventos-hoy').textContent = 'Error';
        document.getElementById('eventos-semana').textContent = 'Error';
    });
}

function cargarUltimosEventos() {
    // Cargar últimos eventos del API
    fetch('/auditoria/api/estadisticas/')
    .then(response => response.json())
    .then(data => {
        if (data.ultimos_eventos && data.ultimos_eventos.length > 0) {
            let html = '<div class="table-responsive"><table class="table table-sm table-hover">';
            html += '<thead class="table-light"><tr>';
            html += '<th>Fecha</th><th>Usuario</th><th>Acción</th><th>Modelo</th><th>IP</th>';
            html += '</tr></thead><tbody>';
            
            data.ultimos_eventos.forEach(evento => {
                const fecha = new Date(evento.fecha_hora).toLocaleString();
                const accionTraducida = traducirAccion(evento.accion_realizada);
                const colorAccion = obtenerColorAccion(evento.accion_realizada);
                html += `<tr>
                    <td><small>${fecha}</small></td>
                    <td><strong>${evento.usuario__username}</strong></td>
                    <td><span class="badge bg-${colorAccion}">${accionTraducida}</span></td>
                    <td>${evento.modelo_afectado}</td>
                    <td><small class="text-muted">${evento.ip_address}</small></td>
                </tr>`;
            });
            
            html += '</tbody></table></div>';
            document.getElementById('ultimos-eventos').innerHTML = html;
        } else {
            document.getElementById('ultimos-eventos').innerHTML = `
                <div class="text-center">
                    <p class="text-muted">No hay eventos registrados aún</p>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Error cargando últimos eventos:', error);
        document.getElementById('ultimos-eventos').innerHTML = `
            <div class="alert alert-danger">Error al cargar los eventos</div>
        `;
    });
}