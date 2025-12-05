from django.shortcuts import get_object_or_404
# Vista para mostrar detalles de una madre
from .models import Madre

def detalle_madre(request, madre_id):
    madre = get_object_or_404(Madre, id=madre_id)
    return render(request, 'gestion_some/detalle_madre.html', {'madre': madre})
from django.shortcuts import get_object_or_404
def editar_madre(request, madre_id):
    madre = get_object_or_404(Madre, id=madre_id)
    if request.method == 'POST':
        madre.nombre = request.POST.get('nombre')
        madre.rut = request.POST.get('rut')
        madre.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        madre.comuna = request.POST.get('comuna')
        madre.cesfam = request.POST.get('cesfam')
        madre.direccion = request.POST.get('direccion')
        madre.telefono = request.POST.get('telefono')
        madre.antecedentes_obstetricos = request.POST.get('antecedentes_obstetricos')
        madre.atenciones_clinicas = request.POST.get('atenciones_clinicas')
        madre.acompañante = request.POST.get('acompañante')
        madre.save()
        return redirect('lista_madres')
    return render(request, 'gestion_some/editar_madre.html', {'madre': madre})

def eliminar_madre(request, madre_id):
    madre = get_object_or_404(Madre, id=madre_id)
    if request.method == 'POST':
        madre.delete()
        return redirect('lista_madres')
    return render(request, 'gestion_some/eliminar_madre.html', {'madre': madre})
from django.shortcuts import render
from .models import Madre

from django.shortcuts import redirect

def crear_madre(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        comuna = request.POST.get('comuna')
        cesfam = request.POST.get('cesfam')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        antecedentes_obstetricos = request.POST.get('antecedentes_obstetricos')
        atenciones_clinicas = request.POST.get('atenciones_clinicas')
        acompanante = request.POST.get('acompañante')
        Madre.objects.create(
            nombre=nombre,
            rut=rut,
            fecha_nacimiento=fecha_nacimiento,
            comuna=comuna,
            cesfam=cesfam,
            direccion=direccion,
            telefono=telefono,
            antecedentes_obstetricos=antecedentes_obstetricos,
            atenciones_clinicas=atenciones_clinicas,
            acompañante=acompanante
        )
        return redirect('lista_madres')
    return render(request, 'gestion_some/crear_madre.html')

def lista_madres(request):
    madres = Madre.objects.all()
    return render(request, 'gestion_some/lista_madres.html', {'madres': madres})
