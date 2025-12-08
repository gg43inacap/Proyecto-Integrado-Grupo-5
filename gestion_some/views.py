from django.shortcuts import get_object_or_404, render, redirect # Funciones para buscar objetos, mostrar páginas y redirigir
# Importa el modelo Madre
from .models import Madre
from auditoria.models import registrar_evento_auditoria
# pylint: disable=no-member
# pyright: reportGeneralTypeIssues=false

# Vista para mostrar los detalles de una madre

def detalle_madre(request, madre_id): # Muestra los detalles de una madre
    madre = get_object_or_404(Madre, id=madre_id) # Obtiene la madre o devuelve 404
    return render(request, 'gestion_some/detalle_madre.html', {'madre': madre}) # Muestra la página de detalles de la madre

# Vista para editar los datos de una madre

def editar_madre(request, madre_id): # Edita los datos de una madre
    madre = get_object_or_404(Madre, id=madre_id) # Obtiene la madre o devuelve 404
    if request.method == 'POST': # Si el formulario ha sido enviado
        madre.nombre = request.POST.get('nombre') # Actualiza el nombre
        madre.rut = request.POST.get('rut') # Actualiza el RUT
        madre.fecha_nacimiento = request.POST.get('fecha_nacimiento') # Actualiza la fecha de nacimiento
        madre.comuna = request.POST.get('comuna') # Actualiza la comuna
        madre.cesfam = request.POST.get('cesfam') # Actualiza el CESFAM
        madre.prevision = request.POST.get('prevision') # Actualiza la previsión
        madre.direccion = request.POST.get('direccion') # Actualiza la dirección
        madre.telefono = request.POST.get('telefono') # Actualiza el teléfono
        madre.antecedentes_obstetricos = request.POST.get('antecedentes_obstetricos') # Actualiza los antecedentes obstétricos
        madre.atenciones_clinicas = request.POST.get('atenciones_clinicas') # Actualiza las atenciones clínicas
        madre.acompanante = request.POST.get('acompanante') # Actualiza el acompañante
        madre.save() # Guarda los cambios en la base de datos
        registrar_evento_auditoria(
            usuario=request.user,
            accion_realizada='UPDATE',
            modelo_afectado='Madre',
            registro_id=madre.id,
            detalles_cambio=f"Madre editada: {madre.nombre} (RUT: {madre.rut})",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return redirect('lista_madres') # Redirige a la lista de madres después de guardar
    return render(request, 'gestion_some/editar_madre.html', {'madre': madre}) # Muestra el formulario de edición

# Vista para eliminar una madre

def eliminar_madre(request, madre_id): # Elimina una madre
    madre = get_object_or_404(Madre, id=madre_id) # Obtiene la madre o devuelve 404
    if request.method == 'POST': # Si se confirma la eliminación
        nombre = madre.nombre
        rut = madre.rut
        id_madre = madre.id
        madre.delete() # Elimina la madre de la base de datos
        registrar_evento_auditoria(
            usuario=request.user,
            accion_realizada='DELETE',
            modelo_afectado='Madre',
            registro_id=id_madre,
            detalles_cambio=f"Madre eliminada: {nombre} (RUT: {rut})",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return redirect('lista_madres') # Redirige a la lista de madres después de eliminar
    return render(request, 'gestion_some/eliminar_madre.html', {'madre': madre}) # Muestra la página de confirmación de eliminación

# Vista para crear una nueva madre

def crear_madre(request): # Crea una nueva madre
    if request.method == 'POST': #  Si el formulario ha sido enviado
        nombre = request.POST.get('nombre') #   Obtiene el nombre del formulario
        rut = request.POST.get('rut') # Obtiene el RUT del formulario
        fecha_nacimiento = request.POST.get('fecha_nacimiento') # Obtiene la fecha de nacimiento del formulario
        comuna = request.POST.get('comuna') # Obtiene la comuna del formulario
        cesfam = request.POST.get('cesfam') # Obtiene el CESFAM del formulario
        direccion = request.POST.get('direccion') # Obtiene la dirección del formulario
        telefono = request.POST.get('telefono') # Obtiene el teléfono del formulario
        antecedentes_obstetricos = request.POST.get('antecedentes_obstetricos') # Obtiene los antecedentes obstétricos del formulario
        atenciones_clinicas = request.POST.get('atenciones_clinicas') # Obtiene las atenciones clínicas del formulario
        acompanante = request.POST.get('acompanante') # Obtiene el acompañante del formulario
        madre = Madre.objects.create(
            nombre=nombre,
            rut=rut,
            fecha_nacimiento=fecha_nacimiento,
            comuna=comuna,
            cesfam=cesfam,
            direccion=direccion,
            telefono=telefono,
            antecedentes_obstetricos=antecedentes_obstetricos,
            atenciones_clinicas=atenciones_clinicas,
            acompanante=acompanante
        )
        registrar_evento_auditoria(
            usuario=request.user,
            accion_realizada='CREATE',
            modelo_afectado='Madre',
            registro_id=madre.id,
            detalles_cambio=f"Madre creada: {madre.nombre} (RUT: {madre.rut})",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return redirect('lista_madres') # Redirige a la lista de madres después de crear
    return render(request, 'gestion_some/crear_madre.html') # Muestra el formulario de creación

def lista_madres(request): # Lista todas las madres
    madres = Madre.objects.all()
    return render(request, 'gestion_some/lista_madres.html', {'madres': madres}) # Muestra la página con la lista de madres
