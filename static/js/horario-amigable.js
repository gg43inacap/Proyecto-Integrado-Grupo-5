// Horario amigable personalizado

class HorarioAmigable {
    constructor(input) {
        this.input = input;
        this.horario = null;
        this.hora = 0;
        this.minuto = 0;
        this.estaAbierto = false;
        
        // Parsear hora inicial si existe
        if (input.value) {
            const partes = input.value.split(':');
            if (partes.length >= 2) {
                this.hora = parseInt(partes[0]) || 0;
                this.minuto = parseInt(partes[1]) || 0;
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
            if (this.estaAbierto && 
                !this.input.contains(e.target) && 
                !this.horario?.contains(e.target)) {
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
    
    mostrar() {
        if (this.estaAbierto || this.horario) return;
        
        this.estaAbierto = true;
        this.horario = document.createElement('div');
        this.horario.className = 'mini-horario';
        
        this.renderizar();
        
        // Posicionar el horario inteligentemente
        const rect = this.input.getBoundingClientRect();
        const alturaHorario = 280;
        const alturaVentana = window.innerHeight;
        const espacioAbajo = alturaVentana - rect.bottom;
        const espacioArriba = rect.top;
        
        this.horario.style.position = 'fixed';
        this.horario.style.left = rect.left + 'px';
        this.horario.style.zIndex = '9999';
        
        // Decidir si mostrar arriba o abajo del input
        if (espacioAbajo >= alturaHorario) {
            this.horario.style.top = (rect.bottom + 2) + 'px';
        } else if (espacioArriba >= alturaHorario) {
            this.horario.style.top = (rect.top - alturaHorario - 2) + 'px';
        } else {
            this.horario.style.top = (rect.bottom + 2) + 'px';
        }
        
        document.body.appendChild(this.horario);
        
        // Verificar si el horario está visible completamente
        setTimeout(() => {
            const horarioRect = this.horario.getBoundingClientRect();
            const horarioAbajo = horarioRect.bottom;
            
            if (horarioAbajo > alturaVentana) {
                const cantidadScroll = horarioAbajo - alturaVentana + 20;
                window.scrollBy({
                    top: cantidadScroll,
                    behavior: 'smooth'
                });
            }
        }, 50);
        
        // Evitar que clics dentro del horario lo cierren
        this.horario.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
    
    ocultar() {
        if (this.horario) {
            document.body.removeChild(this.horario);
            this.horario = null;
        }
        this.estaAbierto = false;
    }
    
    formatearNumero(num) {
        return num.toString().padStart(2, '0');
    }
    
    actualizarDisplay() {
        const display = this.horario.querySelector('.mini-horario-display');
        const horaValor = this.horario.querySelector('[data-tipo="hora"]');
        const minutoValor = this.horario.querySelector('[data-tipo="minuto"]');
        
        if (display) {
            display.textContent = `${this.formatearNumero(this.hora)}:${this.formatearNumero(this.minuto)}`;
        }
        if (horaValor) {
            horaValor.textContent = this.formatearNumero(this.hora);
        }
        if (minutoValor) {
            minutoValor.textContent = this.formatearNumero(this.minuto);
        }
    }
    
    incrementarHora() {
        this.hora = (this.hora + 1) % 24;
        this.actualizarDisplay();
    }
    
    decrementarHora() {
        this.hora = (this.hora - 1 + 24) % 24;
        this.actualizarDisplay();
    }
    
    incrementarMinuto() {
        this.minuto = (this.minuto + 1) % 60;
        this.actualizarDisplay();
    }
    
    decrementarMinuto() {
        this.minuto = (this.minuto - 1 + 60) % 60;
        this.actualizarDisplay();
    }
    
    establecerHoraActual() {
        const ahora = new Date();
        this.hora = ahora.getHours();
        this.minuto = ahora.getMinutes();
        this.actualizarDisplay();
    }
    
    confirmar() {
        const valorFormateado = `${this.formatearNumero(this.hora)}:${this.formatearNumero(this.minuto)}`;
        this.input.value = valorFormateado;
        this.ocultar();
    }
    
    renderizar() {
        this.horario.innerHTML = `
            <div class="mini-horario-header">
                Seleccionar Hora
            </div>
            <div class="mini-horario-body">
                <div class="mini-horario-display">
                    ${this.formatearNumero(this.hora)}:${this.formatearNumero(this.minuto)}
                </div>
                <div class="mini-horario-controles">
                    <div class="mini-horario-grupo">
                        <div class="mini-horario-label">Hora</div>
                        <div class="mini-horario-botones">
                            <button type="button" class="mini-horario-btn" data-action="hora-incrementar">▲</button>
                            <div class="mini-horario-valor" data-tipo="hora">${this.formatearNumero(this.hora)}</div>
                            <button type="button" class="mini-horario-btn" data-action="hora-decrementar">▼</button>
                        </div>
                    </div>
                    <div class="mini-horario-grupo">
                        <div class="mini-horario-label">Minuto</div>
                        <div class="mini-horario-botones">
                            <button type="button" class="mini-horario-btn" data-action="minuto-incrementar">▲</button>
                            <div class="mini-horario-valor" data-tipo="minuto">${this.formatearNumero(this.minuto)}</div>
                            <button type="button" class="mini-horario-btn" data-action="minuto-decrementar">▼</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mini-horario-footer">
                <button type="button" class="mini-horario-btn-accion mini-horario-btn-ahora" data-action="ahora">Ahora</button>
                <button type="button" class="mini-horario-btn-accion mini-horario-btn-ok" data-action="ok">OK</button>
            </div>
        `;
        
        // Event listeners para botones de incremento/decremento
        this.horario.querySelector('[data-action="hora-incrementar"]').addEventListener('click', () => {
            this.incrementarHora();
        });
        
        this.horario.querySelector('[data-action="hora-decrementar"]').addEventListener('click', () => {
            this.decrementarHora();
        });
        
        this.horario.querySelector('[data-action="minuto-incrementar"]').addEventListener('click', () => {
            this.incrementarMinuto();
        });
        
        this.horario.querySelector('[data-action="minuto-decrementar"]').addEventListener('click', () => {
            this.decrementarMinuto();
        });
        
        // Event listeners para botones de acción
        this.horario.querySelector('[data-action="ahora"]').addEventListener('click', () => {
            this.establecerHoraActual();
        });
        
        this.horario.querySelector('[data-action="ok"]').addEventListener('click', () => {
            this.confirmar();
        });
    }
}

// Auto-inicializar al cargar la página (para formularios normales)
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.horario-amigable').forEach(input => {
                if (!input.dataset.horarioIniciado) {
                    new HorarioAmigable(input);
                    input.dataset.horarioIniciado = 'true';
                }
            });
        });
    }
}