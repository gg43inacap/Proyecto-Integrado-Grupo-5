
# pylint: disable=no-member
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Auditoria

# ===============================
# Auditoría: SOLO CONSULTA/VISUALIZACIÓN
# ===============================
# Los registros de auditoría se crean automáticamente por el sistema
# Los auditores SOLO pueden consultar, NO crear/editar/eliminar

def tiene_acceso_auditoria(user):
    """Verifica si el usuario tiene acceso a auditoría"""
    if not user.is_authenticated:
        return False
    # Permitir acceso a AUDITORIA, ADMIN, superusers y modo demo
    return (getattr(user, 'role', None) in ['AUDITORIA', 'ADMIN'] or 
            user.is_superuser or 
            hasattr(user, 'is_demo_mode'))

# El dashboard se maneja en la app 'roles' - panel_AUDITORIA.html
# Esta app solo proporciona vistas de consulta de datos

@login_required
def lista_auditorias(request):
    """
    Lista todos los registros de auditoría con filtros.
    Acceso para usuarios AUDITORIA, ADMIN y superusers.
    SOLO CONSULTA - No permite crear/editar/eliminar.
    """
    if not tiene_acceso_auditoria(request.user):
        return HttpResponseForbidden('Acceso denegado. Se requiere rol AUDITORIA o ADMIN.')
    
    # Obtener parámetros de filtro
    accion_filtro = request.GET.get('accion', '').strip()
    modelo_filtro = request.GET.get('modelo', '').strip()
    usuario_filtro = request.GET.get('usuario', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    orden = request.GET.get('orden', '-fecha_hora')  # Por defecto más reciente primero
    
    # Aplicar filtros
    logs = Auditoria.objects.all()
    
    # OCULTAR actividad del SUPERADMIN - debe ser invisible para todos los demás usuarios
    if not request.user.is_superuser:
        logs = logs.exclude(usuario__is_superuser=True)
    
    if accion_filtro:
        logs = logs.filter(accion_realizada=accion_filtro)
    if modelo_filtro:
        logs = logs.filter(modelo_afectado=modelo_filtro)
    if usuario_filtro:
        logs = logs.filter(usuario__username__icontains=usuario_filtro)
    if fecha_desde:
        try:
            logs = logs.filter(fecha_hora__date__gte=fecha_desde)
        except:
            pass  # Ignorar errores de fecha inválida
    if fecha_hasta:
        try:
            logs = logs.filter(fecha_hora__date__lte=fecha_hasta)
        except:
            pass  # Ignorar errores de fecha inválida
    
    # Aplicar ordenamiento
    orden_validos = ['fecha_hora', '-fecha_hora', 'usuario__username', '-usuario__username', 
                     'accion_realizada', '-accion_realizada', 'modelo_afectado', '-modelo_afectado']
    if orden in orden_validos:
        logs = logs.order_by(orden)
    else:
        logs = logs.order_by('-fecha_hora')
    
    # Estadísticas para el contexto
    total_eventos = logs.count()
    acciones_disponibles = Auditoria.objects.values_list('accion_realizada', flat=True).distinct().order_by('accion_realizada')
    
    # Debug: imprimir acciones disponibles
    print(f"DEBUG - Acciones disponibles: {list(acciones_disponibles)}")
    
    context = {
        'logs': logs,
        'total_eventos': total_eventos,
        'acciones_disponibles': acciones_disponibles,
        'filtros': {
            'accion': accion_filtro,
            'modelo': modelo_filtro, 
            'usuario': usuario_filtro,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'orden': orden,
        }
    }
    
    return render(request, 'auditoria/lista_auditorias.html', context)

@login_required
def detalle_auditoria(request, auditoria_id):
    """
    Muestra el detalle de un registro de auditoría.
    Acceso para usuarios AUDITORIA, ADMIN y superusers.
    SOLO CONSULTA - No permite modificaciones.
    """
    if not tiene_acceso_auditoria(request.user):
        return HttpResponseForbidden('Acceso denegado. Se requiere rol AUDITORIA o ADMIN.')
    try:
        log = Auditoria.objects.get(pk=auditoria_id)
    except Auditoria.DoesNotExist:
        return HttpResponse('Registro de auditoría no encontrado.', status=404)
    return render(request, 'auditoria/detalle_auditoria.html', {'log': log})

@login_required
def estadisticas_auditoria_api(request):
    """
    API para obtener estadísticas reales de auditoría
    Devuelve datos en formato JSON para el dashboard
    """
    if not tiene_acceso_auditoria(request.user):
        return JsonResponse({'error': 'Acceso denegado'}, status=403)
    
    # Fecha de hoy
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de esta semana
    
    # Obtener queryset base (ocultar SUPERADMIN si no eres superuser)
    if request.user.is_superuser:
        base_queryset = Auditoria.objects.all()
    else:
        base_queryset = Auditoria.objects.exclude(usuario__is_superuser=True)
    
    # Calcular estadísticas reales
    total_eventos = base_queryset.count()
    eventos_hoy = base_queryset.filter(fecha_hora__date=hoy).count()
    eventos_semana = base_queryset.filter(fecha_hora__date__gte=inicio_semana).count()
    
    # Estadísticas adicionales
    eventos_por_accion = list(
        base_queryset.values('accion_realizada')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')[:5]
    )
    
    # Actividad de los últimos 7 días
    actividad_semanal = []
    for i in range(7):
        fecha = hoy - timedelta(days=i)
        eventos_dia = base_queryset.filter(fecha_hora__date=fecha).count()
        actividad_semanal.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'eventos': eventos_dia
        })
    
    # Últimos 5 eventos (excluyendo SUPERADMIN si no eres superuser)
    ultimos_eventos = []
    for evento in base_queryset.select_related('usuario').order_by('-fecha_hora')[:5]:
        ultimos_eventos.append({
            'id': evento.id,
            'usuario': evento.usuario.username if evento.usuario else 'Sistema',
            'accion': evento.accion_realizada,
            'modelo': evento.modelo_afectado,
            'fecha': evento.fecha_hora.strftime('%d/%m/%Y %H:%M'),
        })
    
    data = {
        'total_eventos': total_eventos,
        'eventos_hoy': eventos_hoy,
        'eventos_semana': eventos_semana,
        'eventos_por_accion': eventos_por_accion,
        'actividad_semanal': actividad_semanal,
        'ultimos_eventos': ultimos_eventos,
        'fecha_consulta': timezone.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    
    return JsonResponse(data)

# Nota: No existen vistas para crear, editar ni eliminar logs de auditoría.
# El registro es automático y la auditoría es solo de consulta.

# ===============================
# Vista temporal para crear auditoría manualmente
# ===============================

# ===============================
# NOTA IMPORTANTE:
# ===============================
# Los registros de auditoría se crean AUTOMÁTICAMENTE
# cuando se realizan acciones en el sistema.
# Los auditores SOLO pueden CONSULTAR, no crear/editar/eliminar.
# 
# Para crear datos de prueba, use el shell de Django:
# python manage.py shell
# >>> from auditoria.models import registrar_evento_auditoria
# >>> registrar_evento_auditoria(...)
