// Calendario amigable personalizado para 720p

class CalendarioAmigable {
    constructor(input) {
        this.input = input;
        this.calendario = null;
        this.fechaActual = new Date();
        this.fechaSeleccionada = null;
        this.estaAbierto = false;
        
        // Parsear fecha inicial si existe
        if (input.value) {
            const partes = input.value.split('/');
            if (partes.length === 3) {
                this.fechaSeleccionada = new Date(partes[2], partes[1] - 1, partes[0]);
                this.fechaActual = new Date(this.fechaSeleccionada);
            }
        }
        
        this.init();
    }
    
    init() {
        // Manejar clic en el input para mostrar/ocultar
        this.input.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            if (!this.estaAbierto) {
                this.mostrar();
            }
        });
        
        // Manejar focus para mostrar si no está abierto
        this.input.addEventListener('focus', (e) => {
            e.preventDefault();
            
            // Pequeño delay para evitar conflicto con click
            setTimeout(() => {
                if (!this.estaAbierto) {
                    this.mostrar();
                }
            }, 50);
        });
        
        // Cerrar al hacer clic fuera con mejor control
        document.addEventListener('click', (e) => {
            // Solo cerrar si el calendario está abierto y el clic no es en el input ni en el calendario
            if (this.estaAbierto && 
                !this.input.contains(e.target) && 
                !this.calendario?.contains(e.target)) {
                this.ocultar();
            }
        });
        
        // Cerrar con Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.estaAbierto) {
                this.ocultar();
            }
        });
    }
    
    alternar() {
        if (this.estaAbierto) {
            this.ocultar();
        } else {
            this.mostrar();
        }
    }
    
    mostrar() {
        if (this.estaAbierto || this.calendario) return;
        
        this.estaAbierto = true;
        this.calendario = document.createElement('div');
        this.calendario.className = 'mini-calendario';
        
        this.renderizar();
        
        // Posicionar el calendario inteligentemente
        const rect = this.input.getBoundingClientRect();
        const alturaCalendario = 280; // Altura aproximada del calendario
        const alturaVentana = window.innerHeight;
        const espacioAbajo = alturaVentana - rect.bottom;
        const espacioArriba = rect.top;
        
        this.calendario.style.position = 'fixed';
        this.calendario.style.left = rect.left + 'px';
        this.calendario.style.zIndex = '9999';
        
        // Decidir si mostrar arriba o abajo del input
        if (espacioAbajo >= alturaCalendario) {
            // Hay espacio abajo, mostrar debajo
            this.calendario.style.top = (rect.bottom + 2) + 'px';
        } else if (espacioArriba >= alturaCalendario) {
            // No hay espacio abajo pero sí arriba, mostrar arriba
            this.calendario.style.top = (rect.top - alturaCalendario - 2) + 'px';
        } else {
            // No hay suficiente espacio en ningún lado, mostrar abajo y hacer scroll
            this.calendario.style.top = (rect.bottom + 2) + 'px';
        }
        
        document.body.appendChild(this.calendario);
        
        // Verificar si el calendario está visible completamente después de añadirlo
        setTimeout(() => {
            const calendarioRect = this.calendario.getBoundingClientRect();
            const calendarioAbajo = calendarioRect.bottom;
            
            if (calendarioAbajo > alturaVentana) {
                // El calendario se sale por abajo, hacer scroll suave
                const cantidadScroll = calendarioAbajo - alturaVentana + 20; // 20px de margen
                window.scrollBy({
                    top: cantidadScroll,
                    behavior: 'smooth'
                });
            }
        }, 50);
        
        // Evitar que clics dentro del calendario lo cierren
        this.calendario.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
    
    ocultar() {
        if (this.calendario) {
            document.body.removeChild(this.calendario);
            this.calendario = null;
        }
        this.estaAbierto = false;
    }
    
    renderizar() {
        const nombresMeses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        
        const nombresDias = ['D', 'L', 'M', 'X', 'J', 'V', 'S'];
        
        // Generar opciones para el selector de mes
        const opcionesMes = nombresMeses.map((nombre, index) => 
            `<option value="${index}" ${index === this.fechaActual.getMonth() ? 'selected' : ''}>${nombre}</option>`
        ).join('');
        
        // Generar opciones para el selector de año (desde 1900 hasta año actual + 5)
        const añoActual = new Date().getFullYear();
        const opcionesAño = [];
        for (let año = 1900; año <= añoActual + 5; año++) {
            const seleccionado = año === this.fechaActual.getFullYear() ? 'selected' : '';
            opcionesAño.push(`<option value="${año}" ${seleccionado}>${año}</option>`);
        }
        
        this.calendario.innerHTML = `
            <div class="mini-calendario-header">
                <button type="button" class="mini-calendario-nav" data-action="mes-anterior">‹</button>
                <div class="mini-calendario-selectores">
                    <select class="mini-calendario-select" data-selector="mes">${opcionesMes}</select>
                    <select class="mini-calendario-select" data-selector="año">${opcionesAño.join('')}</select>
                </div>
                <button type="button" class="mini-calendario-nav" data-action="mes-siguiente">›</button>
            </div>
            <div class="mini-calendario-grid">
                ${nombresDias.map(dia => `<div class="mini-calendario-day-header">${dia}</div>`).join('')}
                ${this.renderizarDias()}
            </div>
        `;
        
        // Event listeners para navegación
        this.calendario.querySelector('[data-action="mes-anterior"]').addEventListener('click', () => {
            this.fechaActual.setMonth(this.fechaActual.getMonth() - 1);
            this.renderizar();
        });
        
        this.calendario.querySelector('[data-action="mes-siguiente"]').addEventListener('click', () => {
            this.fechaActual.setMonth(this.fechaActual.getMonth() + 1);
            this.renderizar();
        });
        
        // Event listeners para selectores de mes y año
        this.calendario.querySelector('[data-selector="mes"]').addEventListener('change', (e) => {
            this.fechaActual.setMonth(parseInt(e.target.value));
            this.renderizar();
        });
        
        this.calendario.querySelector('[data-selector="año"]').addEventListener('change', (e) => {
            this.fechaActual.setFullYear(parseInt(e.target.value));
            this.renderizar();
        });
        
        // Event listeners para días
        this.calendario.querySelectorAll('.mini-calendario-day[data-date]').forEach(dia => {
            dia.addEventListener('click', (e) => {
                e.stopPropagation();
                const fecha = new Date(e.target.dataset.date);
                this.seleccionarFecha(fecha);
            });
        });
    }
    
    renderizarDias() {
        const año = this.fechaActual.getFullYear();
        const mes = this.fechaActual.getMonth();
        
        const primerDia = new Date(año, mes, 1);
        const ultimoDia = new Date(año, mes + 1, 0);
        const fechaInicio = new Date(primerDia);
        fechaInicio.setDate(fechaInicio.getDate() - primerDia.getDay());
        
        const dias = [];
        const actual = new Date(fechaInicio);
        const hoy = new Date();
        
        for (let i = 0; i < 42; i++) { // 6 semanas máximo
            const esMesActual = actual.getMonth() === mes;
            const estaSeleccionado = this.fechaSeleccionada && 
                actual.getDate() === this.fechaSeleccionada.getDate() &&
                actual.getMonth() === this.fechaSeleccionada.getMonth() &&
                actual.getFullYear() === this.fechaSeleccionada.getFullYear();
            const esHoy = actual.getDate() === hoy.getDate() &&
                actual.getMonth() === hoy.getMonth() &&
                actual.getFullYear() === hoy.getFullYear();
            
            const clases = ['mini-calendario-day'];
            if (!esMesActual) clases.push('other-month');
            if (estaSeleccionado) clases.push('selected');
            if (esHoy && esMesActual) clases.push('today');
            
            dias.push(`
                <div class="${clases.join(' ')}" data-date="${actual.toISOString()}">
                    ${actual.getDate()}
                </div>
            `);
            
            actual.setDate(actual.getDate() + 1);
            
            if (i >= 34 && actual.getMonth() !== mes) break; // Salir si ya pasamos el mes
        }
        
        return dias.join('');
    }
    
    seleccionarFecha(fecha) {
        this.fechaSeleccionada = fecha;
        const dia = String(fecha.getDate()).padStart(2, '0');
        const mes = String(fecha.getMonth() + 1).padStart(2, '0');
        const año = fecha.getFullYear();
        
        this.input.value = `${dia}/${mes}/${año}`;
        this.ocultar();
        
        // Disparar evento change
        this.input.dispatchEvent(new Event('change'));
    }
}

// Auto-inicializar al cargar la página (para formularios normales)
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.calendario-amigable').forEach(input => {
                if (!input.dataset.calendarioIniciado) {
                    new CalendarioAmigable(input);
                    input.dataset.calendarioIniciado = 'true';
                }
            });
        });
    }
}