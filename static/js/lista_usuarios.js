// Funcionalidad para Lista de Usuarios

document.addEventListener('DOMContentLoaded', function() {
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
    
    // Animación suave para elementos de la tabla
    const tableRows = document.querySelectorAll('.custom-table tbody tr');
    tableRows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.05}s`;
        row.classList.add('fade-in-row');
    });
});

// Agregar clase CSS para animación de filas
const style = document.createElement('style');
style.textContent = `
    .fade-in-row {
        animation: fadeInRow 0.5s ease forwards;
        opacity: 0;
    }
    
    @keyframes fadeInRow {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);