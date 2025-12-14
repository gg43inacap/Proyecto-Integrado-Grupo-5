# Imports
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from auditoria.models import registrar_evento_auditoria
from .models import Madre

# pylint: disable=no-member
# pyright: reportGeneralTypeIssues=false


# Vista para verificar RUT antes de crear/editar madre
def verificar_rut(request):
    return render(request, 'gestion_some/verificar_rut.html')


# API para autocompletar datos de madre por RUT
@require_GET
def api_madre_por_rut(request):
    rut = request.GET.get('rut', '').strip()
    if not rut:
        return JsonResponse({'found': False, 'error': 'RUT no proporcionado'}, status=400)
    try:
        madre = Madre.objects.get(rut=rut)
        data = {
            'found': True,
            'id': madre.id,
            'nombre': madre.nombre,
            'fecha_nacimiento': madre.fecha_nacimiento,
            'comuna': madre.comuna,
            'cesfam': madre.cesfam,
            'prevision': madre.prevision,
            'direccion': madre.direccion,
            'telefono': madre.telefono,
            'antecedentes_obstetricos': madre.antecedentes_obstetricos,
            'migrante': madre.migrante,
            'pueblo_originario': madre.pueblo_originario,
            'alergias': madre.alergias,
            'alergias_si': madre.alergias_si,
        }
        return JsonResponse(data)
    except Madre.DoesNotExist:
        return JsonResponse({'found': False})


# Vista para mostrar los detalles de una madre
def detalle_madre(request, madre_id): # Muestra los detalles de una madre
    madre = get_object_or_404(Madre, id=madre_id) # Obtiene la madre o devuelve 404
    return render(request, 'gestion_some/detalle_madre.html', {'madre': madre}) # Muestra la página de detalles de la madre

# Vista para editar los datos de una madre

def editar_madre(request, madre_id): # Edita los datos de una madre
    madre = get_object_or_404(Madre, id=madre_id) # Obtiene la madre o devuelve 404
    if request.method == 'POST': # Si el formulario ha sido enviado
        madre.nombre = request.POST.get('nombre')
        madre.rut = request.POST.get('rut')
        madre.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        madre.comuna = request.POST.get('comuna')
        madre.cesfam = request.POST.get('cesfam')
        madre.prevision = request.POST.get('prevision')
        madre.direccion = request.POST.get('direccion')
        madre.telefono = request.POST.get('telefono')
        madre.antecedentes_obstetricos = request.POST.get('antecedentes_obstetricos')
        madre.migrante = request.POST.get('migrante') == 'True'
        madre.pueblo_originario = request.POST.get('pueblo_originario') == 'True'
        madre.alergias = request.POST.get('alergias') == 'True'
        madre.alergias_si = request.POST.get('alergias_si')
        madre.save()
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
    # Eliminación física deshabilitada. Si se requiere lógica, implementar aquí (por ahora solo redirige)
    return redirect('lista_madres')

# Vista para crear una nueva madre

def crear_madre(request): # Crea una nueva madre
    if request.method == 'POST': #  Si el formulario ha sido enviado
        madre = Madre.objects.create(
            nombre=request.POST.get('nombre'),
            rut=request.POST.get('rut'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento'),
            comuna=request.POST.get('comuna'),
            cesfam=request.POST.get('cesfam'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            antecedentes_obstetricos=request.POST.get('antecedentes_obstetricos'),
            migrante=request.POST.get('migrante') == 'True',
            pueblo_originario=request.POST.get('pueblo_originario') == 'True',
            alergias=request.POST.get('alergias') == 'True',
            alergias_si=request.POST.get('alergias_si'),
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
