from django.shortcuts import render, get_object_or_404, redirect
from .models import Parto, RN
from .forms import PartoForm, RNForm
from gestion_some.models import Madre  # Importación agregada por claridad
from django.contrib.auth.decorators import login_required

@login_required
def lista_partos(request):
    partos = Parto.objects.select_related('madre').all()
    return render(request, 'partos/lista_partos.html', {'partos': partos})
# Vista para crear un nuevo parto
@login_required
def crear_parto(request):
    if request.method == 'POST':
        form = PartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_partos')
    else:
        form = PartoForm()
    return render(request, 'partos/crear_parto.html', {'form': form})
# Vista para editar un parto existente
@login_required
def editar_parto(request, parto_id):
    parto = get_object_or_404(Parto, id=parto_id)
    if request.method == 'POST':
        form = PartoForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            return redirect('lista_partos')
    else:
        form = PartoForm(instance=parto)
    return render(request, 'partos/editar_parto.html', {'form': form, 'parto': parto})

@login_required
def eliminar_parto(request, parto_id):
    parto = get_object_or_404(Parto, id=parto_id)
    if request.method == 'POST':
        parto.delete()
        return redirect('lista_partos')
    return render(request, 'partos/eliminar_parto.html', {'parto': parto})

@login_required
def detalle_parto(request, parto_id):
    parto = get_object_or_404(Parto, id=parto_id)
    return render(request, 'partos/detalle_parto.html', {'parto': parto})

@login_required
def lista_rns(request):
    rns = RN.objects.select_related('madre', 'parto_asociado').all()
    return render(request, 'partos/lista_rns.html', {'rns': rns})

@login_required
def crear_rn(request):
    if request.method == 'POST':
        form = RNForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_rns')
    else:
        form = RNForm()
    return render(request, 'partos/crear_rn.html', {'form': form})

@login_required
def editar_rn(request, rn_id):
    rn = get_object_or_404(RN, id=rn_id)
    if request.method == 'POST':
        form = RNForm(request.POST, instance=rn)
        if form.is_valid():
            form.save()
            return redirect('lista_rns')
    else:
        form = RNForm(instance=rn)
    return render(request, 'partos/editar_rn.html', {'form': form, 'rn': rn})

@login_required
def eliminar_rn(request, rn_id):
    rn = get_object_or_404(RN, id=rn_id)
    if request.method == 'POST':
        rn.delete()
        return redirect('lista_rns')
    return render(request, 'partos/eliminar_rn.html', {'rn': rn})

@login_required
def detalle_rn(request, rn_id):
    rn = get_object_or_404(RN, id=rn_id)
    return render(request, 'partos/detalle_rn.html', {'rn': rn})
