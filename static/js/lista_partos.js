document.addEventListener('DOMContentLoaded', function() {
    // Estado del filtro
    const toggleFiltro = document.getElementById('toggleFiltro');
    const filtroLabel = document.getElementById('filtroLabel');
    const table = document.getElementById('partosTable');
    const tbody = table ? table.querySelector('tbody') : null;
    
    // Variables para ordenamiento
    let sortColumn = null;
    let sortAscending = true;

    // ===== FUNCIONALIDAD DE FILTRO =====
    if (toggleFiltro && tbody) {
        toggleFiltro.addEventListener('change', function() {
            if (this.checked) {
                // Mostrar solo activos
                filtroLabel.textContent = 'Mostrando: Partos activos';
                
                // Ocultar filas de partos completados
                const filas = tbody.querySelectorAll('tr.parto-row');
                filas.forEach(fila => {
                    const estado = fila.dataset.partoEstado;
                    if (estado === 'completado') {
                        fila.style.display = 'none';
                    }
                });
            } else {
                // Mostrar todos
                filtroLabel.textContent = 'Mostrando: Todos los partos';
                
                // Mostrar todas las filas
                const filas = tbody.querySelectorAll('tr.parto-row');
                filas.forEach(fila => {
                    fila.style.display = '';
                });
            }
        });
    }

    // ===== FUNCIONALIDAD DE ORDENAMIENTO =====
    if (table) {
        const headers = table.querySelectorAll('th.sortable');
        
        headers.forEach(header => {
            header.addEventListener('click', function() {
                const column = this.dataset.column;
                
                // Si es la misma columna, invertir dirección
                if (sortColumn === column) {
                    sortAscending = !sortAscending;
                } else {
                    sortColumn = column;
                    sortAscending = true;
                }
                
                // Actualizar iconos
                headers.forEach(h => {
                    const icon = h.querySelector('.sort-icon');
                    if (icon) {
                        icon.classList.remove('fa-sort-up', 'fa-sort-down');
                        icon.classList.add('fa-sort');
                    }
                });
                
                const icon = this.querySelector('.sort-icon');
                if (icon) {
                    icon.classList.remove('fa-sort');
                    icon.classList.add(sortAscending ? 'fa-sort-up' : 'fa-sort-down');
                }
                
                // Ordenar filas
                sortTable(column, sortAscending);
            });
        });
    }

    function sortTable(column, ascending) {
        if (!tbody) return;
        
        const rows = Array.from(tbody.querySelectorAll('tr.parto-row'));
        
        rows.sort((a, b) => {
            let aValue, bValue;
            
            switch(column) {
                case 'madre':
                    aValue = a.querySelector('[data-madre]')?.dataset.madre || '';
                    bValue = b.querySelector('[data-madre]')?.dataset.madre || '';
                    break;
                case 'fecha':
                    aValue = a.querySelector('[data-fecha]')?.dataset.fecha || '';
                    bValue = b.querySelector('[data-fecha]')?.dataset.fecha || '';
                    break;
                case 'hora':
                    aValue = a.querySelector('[data-hora]')?.dataset.hora || '';
                    bValue = b.querySelector('[data-hora]')?.dataset.hora || '';
                    break;
                case 'tipo':
                    aValue = a.querySelector('[data-tipo]')?.dataset.tipo || '';
                    bValue = b.querySelector('[data-tipo]')?.dataset.tipo || '';
                    break;
                case 'estado':
                    aValue = a.dataset.partoEstado || '';
                    bValue = b.dataset.partoEstado || '';
                    break;
                default:
                    return 0;
            }
            
            // Comparación
            if (aValue < bValue) return ascending ? -1 : 1;
            if (aValue > bValue) return ascending ? 1 : -1;
            return 0;
        });
        
        // Reorganizar el DOM
        rows.forEach(row => tbody.appendChild(row));
    }

    // ===== FUNCIONALIDAD DE COMPLETAR PARTO =====
    document.querySelectorAll('.btn-complete-parto').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            const url = this.dataset.url;
            
            if (url) {
                if (confirm('¿Desea marcar este parto como completado?')) {
                    // Redirigir a la URL de completado
                    window.location.href = url;
                }
            }
        });
    });

    // Botón Back to Top
    const backToTopBtn = document.getElementById('backToTopBtn');

    // Mostrar/ocultar botón según scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });

    // Función para volver al inicio
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});