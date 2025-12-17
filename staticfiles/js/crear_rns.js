function filtrarPartos() {
    // Buscar todos los selects de madre y parto en el formset
    const madreSelects = document.querySelectorAll('[id*="id_"][id*="-madre"]');
    const partoSelects = document.querySelectorAll('[id*="id_"][id*="-parto_asociado"]');
    
    madreSelects.forEach((madreSelect, index) => {
        const partoSelect = partoSelects[index];
        const madreId = madreSelect.value;
        
        if (partoSelect) {
            console.log(`Filtrando partos para formulario ${index}, madre ID:`, madreId);
            
            // Limpiar opciones actuales del select de partos
            partoSelect.innerHTML = '<option value="">Cargando...</option>';
            
            if (madreId) {
                const url = `/partos/ajax/filtrar-partos/?madre_id=${madreId}`;
                
                fetch(url)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Limpiar el select
                        partoSelect.innerHTML = '<option value="">---------</option>';
                        
                        if (data.error) {
                            console.error('Error del servidor:', data.error);
                            const option = new Option(`Error: ${data.error}`, '');
                            option.disabled = true;
                            partoSelect.add(option);
                        } else {
                            data.partos.forEach(parto => {
                                const option = new Option(parto.text, parto.id);
                                partoSelect.add(option);
                            });
                            
                            if (data.partos.length === 0) {
                                const option = new Option('No hay partos activos para esta madre', '');
                                option.disabled = true;
                                partoSelect.add(option);
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error completo:', error);
                        partoSelect.innerHTML = '<option value="">---------</option>';
                        const option = new Option(`Error de conexión: ${error.message}`, '');
                        option.disabled = true;
                        partoSelect.add(option);
                    });
            } else {
                partoSelect.innerHTML = '<option value="">---------</option>';
            }
        }
    });
}

/**
 * Función para mostrar/ocultar el campo de descripción de anomalía
 * según el estado del checkbox de anomalia_congenita
 */
function toggleDescripcionAnomalia(checkbox) {
    const form = checkbox.closest('.ribbon-tab');
    if (!form) return;
    
    const descripcionContainer = form.querySelector('.descripcion-anomalia-container');
    if (!descripcionContainer) return;
    
    const descripcionInput = descripcionContainer.querySelector('input[name*="descripcion_anomalia"]');
    
    if (checkbox.checked) {
        // Mostrar el campo y hacerlo requerido
        descripcionContainer.style.display = 'block';
        if (descripcionInput) {
            descripcionInput.required = true;
            descripcionInput.focus();
        }
        console.log('Campo de descripción de anomalía mostrado');
    } else {
        // Ocultar el campo y limpiar su valor
        descripcionContainer.style.display = 'none';
        if (descripcionInput) {
            descripcionInput.value = '';
            descripcionInput.required = false;
        }
        console.log('Campo de descripción de anomalía oculto y limpiado');
    }
}

/**
 * Función para configurar eventos en un formulario
 */
function setupFormEvents(form) {
    // Buscar el checkbox de anomalia_congenita
    const anomaliaCheckbox = form.querySelector('input[name*="anomalia_congenita"]');
    if (anomaliaCheckbox) {
        anomaliaCheckbox.addEventListener('change', function() {
            toggleDescripcionAnomalia(this);
        });
        
        // Aplicar el estado inicial (si ya está marcado al cargar)
        if (anomaliaCheckbox.checked) {
            toggleDescripcionAnomalia(anomaliaCheckbox);
        }
    }
    
    // Configurar evento de filtrado de partos
    const madreSelect = form.querySelector('[id*="-madre"]');
    if (madreSelect) {
        madreSelect.addEventListener('change', filtrarPartos);
    }
}

function addForm() {
    if (formIndex >= maxForms) {
        alert('¡Límite máximo alcanzado! Incluso la esposa de Apu necesitaría un descanso después de 10 bebés 😅');
        return;
    }
    
    const container = document.getElementById('formset-container');
    const lastForm = container.querySelector('.ribbon-tab:last-child');
    
    if (lastForm) {
        // Clonar el último formulario
        const newForm = lastForm.cloneNode(true);
        
        // Actualizar el índice del formulario
        newForm.setAttribute('data-form-index', formIndex);
        
        // Actualizar el título
        const title = newForm.querySelector('h5');
        title.innerHTML = `<i class="fas fa-baby"></i> Recién Nacido ${formIndex + 1}`;
        
        // Limpiar valores de todos los campos
        const inputs = newForm.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            // Actualizar nombres e IDs
            const oldName = input.getAttribute('name');
            const oldId = input.getAttribute('id');
            
            if (oldName) {
                const newName = oldName.replace(/-\d+-/, `-${formIndex}-`);
                input.setAttribute('name', newName);
            }
            
            if (oldId) {
                const newId = oldId.replace(/-\d+-/, `-${formIndex}-`);
                input.setAttribute('id', newId);
            }
            
            // Limpiar valores
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });
        
        // Actualizar labels
        const labels = newForm.querySelectorAll('label');
        labels.forEach(label => {
            const forAttr = label.getAttribute('for');
            if (forAttr) {
                const newFor = forAttr.replace(/-\d+-/, `-${formIndex}-`);
                label.setAttribute('for', newFor);
            }
        });
        
        // Asegurar alineación correcta de los checkboxes/switches
        const checkboxContainers = newForm.querySelectorAll('.form-check.form-switch');
        checkboxContainers.forEach(container => {
            const parentCol = container.closest('.col-md-6');
            if (parentCol) {
                parentCol.classList.add('d-flex', 'align-items-center');
                parentCol.style.minHeight = '58px';
            }
        });
        
        // Asegurar que tenga botón de quitar
        const removeBtn = newForm.querySelector('.remove-form-btn');
        if (!removeBtn) {
            const titleDiv = newForm.querySelector('.d-flex');
            titleDiv.innerHTML += `
                <button type="button" class="btn btn-sm btn-outline-danger remove-form-btn" onclick="removeForm(this)">
                    <i class="fas fa-times"></i> Quitar
                </button>
            `;
        }
        
        // Agregar al contenedor
        container.appendChild(newForm);
        
        // Aplicar formato automático a fecha y hora del nuevo formulario
        const nuevoFechaInput = newForm.querySelector('input[name*="fecha_nacimiento"]');
        if (nuevoFechaInput) {
            nuevoFechaInput.addEventListener('input', function() { formatoFecha(this); });
            nuevoFechaInput.setAttribute('maxlength', '10');
        }
        
        const nuevoHoraInput = newForm.querySelector('input[name*="hora_nacimiento"]');
        if (nuevoHoraInput) {
            nuevoHoraInput.addEventListener('input', function() { formatoHora(this); });
            nuevoHoraInput.setAttribute('maxlength', '5');
        }
        
        // Configurar eventos para el nuevo formulario
        const newMadreSelect = newForm.querySelector('[id*="-madre"]');
        if (newMadreSelect) {
            newMadreSelect.addEventListener('change', filtrarPartos);
        }
        
    // Incrementar contador
    formIndex++;
        
        // Actualizar el campo TOTAL_FORMS
        const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
    if (totalFormsInput) totalFormsInput.value = formIndex;
        
        // Scroll al nuevo formulario
        newForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        console.log(`Formulario añadido. Total forms: ${formIndex}`);
    }
}

function removeForm(button) {
    const container = document.getElementById('formset-container');
    
    if (container.children.length <= 1) {
        alert('Debe haber al menos un recién nacido para registrar.');
        return;
    }
    
    if (confirm('¿Está seguro de que desea quitar este formulario?')) {
        const form = button.closest('.ribbon-tab');
        form.remove();
        
        // Esta función es clave: renumera IDs, Names, Títulos y actualiza formIndex
        updateFormIndices();
        
        // Actualizar el TOTAL_FORMS para Django
        const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
        if (totalFormsInput) {
            totalFormsInput.value = container.querySelectorAll('.ribbon-tab').length;
        }
    }
}

function updateFormTitles() {
    const forms = document.querySelectorAll('.ribbon-tab');
    forms.forEach((form, index) => {
        const title = form.querySelector('h5');
        if (title) {
            title.innerHTML = `<i class="fas fa-baby"></i> Recién Nacido ${index + 1}`;
        }
    });
}

/**
 * Función para actualizar títulos, data-indices, IDs y names 
 * después de una eliminación.
 */
function updateFormIndices() {
    const forms = document.querySelectorAll('.ribbon-tab');
    
    forms.forEach((form, index) => {
        // Actualizar título (Recién Nacido 1, 2, etc.)
        const title = form.querySelector('h5');
        if (title) {
            title.innerHTML = `<i class="fas fa-baby"></i> Recién Nacido ${index + 1}`;
        }

        // Actualizar nombres e IDs de los inputs para Django
        const elements = form.querySelectorAll('input, select, textarea, label');
        elements.forEach(el => {
            const attrs = ['name', 'id', 'for'];
            attrs.forEach(attr => {
                const val = el.getAttribute(attr);
                if (val) {
                    // Reemplaza el índice viejo por el nuevo (index actual del loop)
                    el.setAttribute(attr, val.replace(/-\d+-/, `-${index}-`));
                }
            });
        });

        form.setAttribute('data-form-index', index);
    });

    // REINICIAR EL CONTADOR GLOBAL al número real de formularios
    formIndex = forms.length;
}

document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('formset-container');
    const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');

    if (container) {
        // Obtener todos los formularios renderizados
        let forms = container.querySelectorAll('.ribbon-tab');

        // Si hay más de uno por error del servidor o caché, dejamos solo el primero
        if (forms.length > 1) {
            for (let i = 1; i < forms.length; i++) {
                forms[i].remove();
            }
            // Actualizar la lista después de borrar
            forms = container.querySelectorAll('.ribbon-tab');
        }

        // Inicializar eventos para el único formulario que quedó
        forms.forEach(form => {
            setupFormEvents(form);
        });

        // IMPORTANTE: Sincronizar el contador global y el input de Django
        formIndex = 1; 
        if (totalFormsInput) {
            totalFormsInput.value = 1;
        }
    }

    // Configurar el botón de añadir
    const addButton = document.getElementById('add-form-btn');
    if (addButton) {
        addButton.addEventListener('click', addForm);
    }
});