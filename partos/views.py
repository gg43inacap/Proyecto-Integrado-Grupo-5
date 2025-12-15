# Importaciones necesarias
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Parto, RN
from .forms import PartoForm, PartoCreateForm, RNForm, RNFormSet
from auditoria.models import registrar_evento_auditoria
from datetime import datetime
# Vista para crear múltiples RN en una sola pantalla
# pylint: disable=no-member
@login_required
def crear_rns(request):
    parto_id = request.GET.get('parto_id')
    initial = {}
    if parto_id:
        try:
            parto = Parto.objects.get(id=parto_id)
            initial['parto_asociado'] = parto
            initial['madre'] = parto.madre
        except Parto.DoesNotExist:
            parto = None
    else:
        parto = None
    RNFormSetLocal = RNFormSet
    if request.method == 'POST':
        formset = RNFormSetLocal(request.POST, queryset=RN.objects.none())
        if formset.is_valid():
            rns = formset.save()
            for rn in rns:
                registrar_evento_auditoria(
                    usuario=request.user,
                    accion_realizada='CREATE',
                    modelo_afectado='RN',
                    registro_id=rn.id,
                    detalles_cambio=f"RN creado para madre ID: {rn.madre.id if rn.madre else ''}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
            return redirect('lista_rns')
    else:
        formset = RNFormSetLocal(queryset=RN.objects.none(), initial=[initial]*RNFormSetLocal.extra)
    return render(request, 'partos/crear_rns.html', {'formset': formset, 'parto': parto})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Parto, RN
from .forms import PartoForm, RNForm
from django.contrib.auth.decorators import login_required
from auditoria.models import registrar_evento_auditoria


@login_required
def api_estadisticas_matrona(request):
    """API REST que devuelve estadísticas relacionadas con partos y recién nacidos para el panel de Matrona."""
    try:
        hoy = timezone.now().date()
        
        # Estadísticas de partos
        total_partos = Parto.objects.count()
        partos_activos = Parto.objects.filter(estado='activo').count()
        # Filtrar por fecha_ingreso (puede ser null)
        partos_hoy = Parto.objects.filter(fecha_ingreso=hoy).count()
        partos_mes = Parto.objects.filter(
            fecha_ingreso__year=hoy.year, 
            fecha_ingreso__month=hoy.month
        ).count()
        
        # Estadísticas de recién nacidos
        total_rns = RN.objects.count()
        rns_hoy = RN.objects.filter(fecha_nacimiento=hoy).count()
        rns_mes = RN.objects.filter(
            fecha_nacimiento__year=hoy.year,
            fecha_nacimiento__month=hoy.month
        ).count()

        return JsonResponse({
            'total_partos': total_partos,
            'partos_activos': partos_activos,
            'partos_hoy': partos_hoy,
            'partos_mes': partos_mes,
            'total_rns': total_rns,
            'rns_hoy': rns_hoy,
            'rns_mes': rns_mes,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def lista_partos(request):
    # Mostrar todos los partos, ordenados por ID descendente (más recientes primero)
    partos = Parto.objects.select_related('madre').all().order_by('-id')
    return render(request, 'partos/lista_partos.html', {'partos': partos})
# Vista para crear un nuevo parto
@login_required
def crear_parto(request):
    parto_guardado = None
    if request.method == 'POST':
        # Hacer una copia mutable del POST data
        post_data = request.POST.copy()
        
        # Convertir fecha_ingreso de DD/MM/AAAA a YYYY-MM-DD si existe
        fecha_ingreso_input = post_data.get('fecha_ingreso')
        if fecha_ingreso_input:
            try:
                fecha_obj = datetime.strptime(fecha_ingreso_input, '%d/%m/%Y')
                post_data['fecha_ingreso'] = fecha_obj.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                pass  # Si ya está en formato correcto o vacío, dejarlo como está
        
        form = PartoCreateForm(post_data)
        if form.is_valid():
            parto = form.save()
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='CREATE',
                modelo_afectado='Parto',
                registro_id=parto.id,
                detalles_cambio=f"Parto creado para madre ID: {parto.madre.id if parto.madre else ''}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            parto_guardado = parto
            form = PartoCreateForm()  # Limpiar el formulario tras guardar
    else:
        form = PartoCreateForm()
    return render(request, 'partos/crear_parto.html', {'form': form, 'parto_guardado': parto_guardado})
# Vista para editar un parto existente
@login_required
def editar_parto(request, parto_id):
    parto = get_object_or_404(Parto, id=parto_id)
    if request.method == 'POST':
        # Hacer una copia mutable del POST data
        post_data = request.POST.copy()
        
        # Convertir fecha_ingreso de DD/MM/AAAA a YYYY-MM-DD si existe
        fecha_ingreso_input = post_data.get('fecha_ingreso')
        if fecha_ingreso_input:
            try:
                fecha_obj = datetime.strptime(fecha_ingreso_input, '%d/%m/%Y')
                post_data['fecha_ingreso'] = fecha_obj.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                pass  # Si ya está en formato correcto o vacío, dejarlo como está
        
        form = PartoForm(post_data, instance=parto)
        if form.is_valid():
            parto_edit = form.save()
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='UPDATE',
                modelo_afectado='Parto',
                registro_id=parto_edit.id,
                detalles_cambio=f"Parto editado para madre ID: {parto_edit.madre.id if parto_edit.madre else ''}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('lista_partos')
    else:
        form = PartoForm(instance=parto)
    return render(request, 'partos/editar_parto.html', {'form': form, 'parto': parto})



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
    parto_id = request.GET.get('parto_id')
    initial = {}
    if parto_id:
        try:
            parto = Parto.objects.get(id=parto_id)
            initial['parto_asociado'] = parto
            initial['madre'] = parto.madre
        except Parto.DoesNotExist:
            pass
    if request.method == 'POST':
        form = RNForm(request.POST)
        if form.is_valid():
            rn = form.save()
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='CREATE',
                modelo_afectado='RN',
                registro_id=rn.id,
                detalles_cambio=f"RN creado para madre ID: {rn.madre.id if rn.madre else ''}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('lista_rns')
    else:
        form = RNForm(initial=initial)
        return render(request, 'partos/crear_rn.html', {'form': form})

@login_required
def filtrar_partos_por_madre(request):
    """Vista AJAX para filtrar partos activos por madre seleccionada"""
    try:
        madre_id = request.GET.get('madre_id')
        print(f"Debug: madre_id recibido = {madre_id}")  # Debug
        
        if madre_id:
            partos = Parto.objects.filter(madre_id=madre_id, estado='activo')
            print(f"Debug: partos encontrados = {partos.count()}")  # Debug
            
            partos_list = []
            for parto in partos:
                partos_list.append({
                    'id': parto.id,
                    'text': f"Parto {parto.id} - {parto.fecha_ingreso.strftime('%d/%m/%Y ')} - {parto.hora_ingreso.strftime('%H:%M')} - {parto.get_tipo_parto_display()}"
                })
        else:
            partos_list = []
        
        print(f"Debug: enviando {len(partos_list)} partos")  # Debug
        return JsonResponse({'partos': partos_list})
        
    except Exception as e:
        print(f"Error en filtrar_partos_por_madre: {e}")
        return JsonResponse({'error': str(e)}, status=500)
@login_required
def editar_rn(request, rn_id):
    rn = get_object_or_404(RN, id=rn_id)
    if request.method == 'POST':
        form = RNForm(request.POST, instance=rn)
        if form.is_valid():
            rn_edit = form.save()
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='UPDATE',
                modelo_afectado='RN',
                registro_id=rn_edit.id,
                detalles_cambio=f"RN editado para madre ID: {rn_edit.madre.id if rn_edit.madre else ''}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('lista_rns')
    else:
        form = RNForm(instance=rn)
    return render(request, 'partos/editar_rn.html', {'form': form, 'rn': rn})



@login_required
def completar_parto(request, parto_id):
    """Vista para marcar un parto como completado"""
    parto = get_object_or_404(Parto, id=parto_id)
    if request.method == 'POST':
        parto.estado = 'completado'
        parto.save()
        
        registrar_evento_auditoria(
            usuario=request.user,
            accion_realizada='UPDATE',
            modelo_afectado='Parto',
            registro_id=parto.id,
            detalles_cambio=f"Parto marcado como completado para madre ID: {parto.madre.id if parto.madre else ''}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return redirect('lista_partos')
    
    return render(request, 'partos/completar_parto.html', {'parto': parto})



@login_required
def detalle_rn(request, rn_id):
    rn = get_object_or_404(RN, id=rn_id)
    return render(request, 'partos/detalle_rn.html', {'rn': rn})
