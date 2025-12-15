// static/js/detalle_rn.js

/**
 * Botón flotante "Back to Top"
 * Se muestra cuando el usuario hace scroll hacia abajo
 */
document.addEventListener('DOMContentLoaded', function() {
    const btnBackToTop = document.getElementById('btnBackToTop');
    
    if (btnBackToTop) {
        // Mostrar/ocultar botón según scroll
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                btnBackToTop.classList.add('show');
            } else {
                btnBackToTop.classList.remove('show');
            }
        });
        
        // Scroll suave al hacer clic
        btnBackToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    console.log('Detalle RN inicializado correctamente 👶');
});
