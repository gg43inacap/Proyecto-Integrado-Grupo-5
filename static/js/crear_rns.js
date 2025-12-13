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
    const form = button.closest('.ribbon-tab');
    const container = document.getElementById('formset-container');
    
    // No permitir eliminar si solo hay un formulario
    if (container.children.length <= 1) {
        alert('Debe haber al menos un recién nacido para registrar.');
        return;
    }
    
    // Confirmar eliminación
    if (confirm('¿Está seguro de que desea quitar este formulario de recién nacido?')) {
        form.remove();
        
        // Actualizar numeración de títulos
        updateFormTitles();
        
        // Actualizar TOTAL_FORMS
        const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
        if (totalFormsInput) {
            totalFormsInput.value = container.children.length;
        }
        
        console.log(`Formulario eliminado. Total forms: ${container.children.length}`);
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
        // 1. Actualizar título visible
        const title = form.querySelector('h5');
        if (title) {
            title.innerHTML = `<i class="fas fa-baby"></i> Recién Nacido ${index + 1}`;
        }

        // 2. Actualizar el índice en los nombres/IDs de los campos
        const elementsToUpdate = form.querySelectorAll('input, select, textarea, label');
        elementsToUpdate.forEach(element => {
            const oldName = element.getAttribute('name');
            const oldId = element.getAttribute('id');
            const oldFor = element.getAttribute('for');

            // Actualizar nombres
            if (oldName) {
                // Reemplaza el número de índice antiguo (ej: -0-, -1-, -2-) por el nuevo
                const newName = oldName.replace(/-\d+-/, `-${index}-`);
                element.setAttribute('name', newName);
            }
            // Actualizar IDs
            if (oldId) {
                const newId = oldId.replace(/-\d+-/, `-${index}-`);
                element.setAttribute('id', newId);
            }
            // Actualizar 'for' de las etiquetas (labels)
            if (oldFor) {
                const newFor = oldFor.replace(/-\d+-/, `-${index}-`);
                element.setAttribute('for', newFor);
            }
        });

        // 3. Actualizar el atributo data-form-index
        form.setAttribute('data-form-index', index);
    });

    // 4. Actualizar la variable global 'formIndex' al nuevo total (para el próximo formulario a crear)
    formIndex = forms.length;
}

// Configurar eventos al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Configurar botón de añadir formulario
    const addButton = document.getElementById('add-form-btn');
    if (addButton) {
        addButton.addEventListener('click', addForm);
    }
    
    // Mostrar solo el primer ribbon si la plantilla renderizó varios
    const container = document.getElementById('formset-container');
    if (container) {
        const forms = Array.from(container.querySelectorAll('.ribbon-tab'));

        // If the template rendered multiple, keep only the first visible and remove others from DOM
        if (forms.length > 1) {
            // Remove all except the first
            forms.slice(1).forEach(f => f.remove());
        }

        // Ensure formIndex and TOTAL_FORMS reflect current visible forms (start at 1)
        formIndex = container.querySelectorAll('.ribbon-tab').length || 1;
        const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
        if (totalFormsInput) totalFormsInput.value = formIndex;

        // Attach filtrarPartos to the madre selects present
        const madreSelects = container.querySelectorAll('[id*="id_"][id*="-madre"]');
        madreSelects.forEach(ms => ms.addEventListener('change', filtrarPartos));
        if (madreSelects.length && madreSelects[0].value) filtrarPartos();
    }
    
    console.log('Formset dinámico inicializado. Listo para partos múltiples! 👶👶👶');
});
