// static/js/lista_rns.js

document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidad de ordenamiento
    const table = document.getElementById('tablaRNs');
    if (table) {
        const headers = table.querySelectorAll('th.sortable');
        
        headers.forEach(header => {
            header.addEventListener('click', function() {
                const column = this.dataset.column;
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr')).filter(row => row.cells.length > 1);
                
                // Determinar dirección del ordenamiento
                const currentSort = this.dataset.sort || 'none';
                const newSort = currentSort === 'asc' ? 'desc' : 'asc';
                
                // Limpiar iconos de todos los headers
                headers.forEach(h => {
                    h.dataset.sort = 'none';
                    const icon = h.querySelector('.sort-icon');
                    if (icon) {
                        icon.className = 'fas fa-sort sort-icon';
                    }
                });
                
                // Actualizar icono del header actual
                this.dataset.sort = newSort;
                const icon = this.querySelector('.sort-icon');
                if (icon) {
                    icon.className = `fas fa-sort-${newSort === 'asc' ? 'up' : 'down'} sort-icon`;
                }
                
                // Ordenar filas
                rows.sort((a, b) => {
                    let aValue, bValue;
                    
                    switch(column) {
                        case 'id':
                            aValue = parseInt(a.cells[0].textContent.replace('#', ''));
                            bValue = parseInt(b.cells[0].textContent.replace('#', ''));
                            break;
                        case 'madre':
                            aValue = a.dataset.madre.toLowerCase();
                            bValue = b.dataset.madre.toLowerCase();
                            break;
                        case 'parto':
                            aValue = parseInt(a.dataset.parto);
                            bValue = parseInt(b.dataset.parto);
                            break;
                        case 'fecha':
                            aValue = new Date(a.dataset.fecha);
                            bValue = new Date(b.dataset.fecha);
                            break;
                        case 'peso':
                            aValue = parseInt(a.dataset.peso) || 0;
                            bValue = parseInt(b.dataset.peso) || 0;
                            break;
                        default:
                            return 0;
                    }
                    
                    if (aValue < bValue) return newSort === 'asc' ? -1 : 1;
                    if (aValue > bValue) return newSort === 'asc' ? 1 : -1;
                    return 0;
                });
                
                // Reordenar el tbody
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    }
    
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
    
    console.log('Lista RNs inicializada correctamente 👶');
});
