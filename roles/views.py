# Imports
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from partos.models import Parto
from gestion_some.models import Madre
from auditoria.models import registrar_evento_auditoria, Auditoria
from .forms import CustomUserForm


# Vista para listar todos los usuarios registrados
@login_required
def listar_usuario(request):
    User = get_user_model()
    # ADMIN no puede ver ni editar SUPERADMIN ni superuser
    if getattr(request.user, 'role', None) == 'ADMIN':
        users = User.objects.exclude(role='SUPERADMIN').exclude(is_superuser=True)
    else:
        users = User.objects.all()
    return render(request, 'roles/lista_usuarios.html', {'users': users})


# Vista principal que muestra el panel según el rol del usuario
@login_required
def dashboard(request):
    # Verificación de seguridad: solo usuarios autenticados con rol válido
    if not request.user.is_authenticated:
        return render(request, 'roles/no_autorizado.html')

    # Permitir a superuser y SUPERADMIN elegir panel con ?rol=
    rol_param = request.GET.get('rol')
    if rol_param and (request.user.is_superuser or getattr(request.user, 'role', None) == 'SUPERADMIN'):
        if rol_param == 'SUPERADMIN' or rol_param == 'ADMIN':
            return render(request, 'roles/panel_admin.html', {'user_role_display': 'Super Administrador' if rol_param == 'SUPERADMIN' else 'Administrador'})
        elif rol_param == 'SOME':
            return render(request, 'roles/panel_some.html', {'user_role_display': 'SOME'})
        elif rol_param == 'MATRONA':
            return render(request, 'roles/panel_matrona.html', {'user_role_display': 'Matrona'})
        elif rol_param == 'SUPERVISOR':
            return render(request, 'roles/panel_supervisor.html', {'user_role_display': 'Supervisor'})
        elif rol_param == 'AUDITORIA':
            return render(request, 'roles/panel_auditoria.html', {'user_role_display': 'Auditoría'})
        else:
            messages.error(request, f'Rol no reconocido: {rol_param}. Acceso denegado.')
            return render(request, 'roles/no_autorizado.html')

    # Si es superuser, mostrar panel especial o de admin por defecto
    if request.user.is_superuser:
        return render(request, 'roles/panel_admin.html', {'user_role_display': 'Super Administrador'})
    rol = getattr(request.user, 'role', None)
    if not rol or rol == '':
        messages.error(request, 'Usuario sin rol asignado. Contacte al administrador.')
        return render(request, 'roles/no_autorizado.html')
    # Renderizar panel según rol verificado
    if rol == 'SUPERADMIN':
        return render(request, 'roles/panel_admin.html', {'user_role_display': 'Super Administrador'})
    elif rol == 'ADMIN':
        return render(request, 'roles/panel_admin.html', {'user_role_display': 'Administrador'})
    elif rol == 'SOME':
        return render(request, 'roles/panel_some.html', {'user_role_display': 'SOME'})
    elif rol == 'MATRONA':
        return render(request, 'roles/panel_matrona.html', {'user_role_display': 'Matrona'})
    elif rol == 'SUPERVISOR':
        return render(request, 'roles/panel_supervisor.html', {'user_role_display': 'Supervisor'})
    elif rol == 'AUDITORIA':
        return render(request, 'roles/panel_auditoria.html', {'user_role_display': 'Auditoría'})
    else:
        messages.error(request, f'Rol no reconocido: {rol}. Acceso denegado.')
        return render(request, 'roles/no_autorizado.html')


# API: Estadísticas para panel admin (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_admin(request):
    User = get_user_model()
    hoy = timezone.now().date()
    hace_una_semana = hoy - timezone.timedelta(days=7)
    
    # Estadísticas básicas
    total_usuarios = User.objects.count()
    usuarios_bloqueados = User.objects.filter(is_active=False).count()
    usuarios_nuevos = User.objects.filter(date_joined__date=hoy).count()
    usuarios_modificados = Auditoria.objects.filter(
        accion_realizada='UPDATE',
        modelo_afectado='Usuario',
        fecha_hora__date__gte=hace_una_semana
    ).values('registro_id').distinct().count()
    
    # Usuarios por rol
    usuarios_admin = User.objects.filter(role='ADMIN').count()
    usuarios_some = User.objects.filter(role='SOME').count()
    usuarios_matrona = User.objects.filter(role='MATRONA').count()
    usuarios_supervisor = User.objects.filter(role='SUPERVISOR').count()
    usuarios_auditoria = User.objects.filter(role='AUDITORIA').count()
    
    # Datos para gráfico de barras (usuarios por rol en el año)
    usuarios_roles_anio = {
        'labels': ['Admin', 'SOME', 'Matrona', 'Supervisor', 'Auditoría', 'Bloqueados'],
        'data': [usuarios_admin, usuarios_some, usuarios_matrona, usuarios_supervisor, usuarios_auditoria, usuarios_bloqueados]
    }
    
    # Datos para gráfico de torta (modificaciones por rol en el mes)
    hoy = timezone.now().date()
    hace_un_mes = hoy - timezone.timedelta(days=30)
    
    admin_cambios = Auditoria.objects.filter(
        usuario__role='ADMIN',
        fecha_hora__date__gte=hace_un_mes
    ).count()
    some_cambios = Auditoria.objects.filter(
        usuario__role='SOME',
        fecha_hora__date__gte=hace_un_mes
    ).count()
    matrona_cambios = Auditoria.objects.filter(
        usuario__role='MATRONA',
        fecha_hora__date__gte=hace_un_mes
    ).count()
    supervisor_cambios = Auditoria.objects.filter(
        usuario__role='SUPERVISOR',
        fecha_hora__date__gte=hace_un_mes
    ).count()
    auditoria_cambios = Auditoria.objects.filter(
        usuario__role='AUDITORIA',
        fecha_hora__date__gte=hace_un_mes
    ).count()
    
    modificaciones_roles_mes = {
        'labels': ['Admin', 'SOME', 'Matrona', 'Supervisor', 'Auditoría'],
        'data': [admin_cambios, some_cambios, matrona_cambios, supervisor_cambios, auditoria_cambios]
    }
    
    return JsonResponse({
        'total_usuarios': total_usuarios,
        'usuarios_bloqueados': usuarios_bloqueados,
        'usuarios_nuevos': usuarios_nuevos,
        'usuarios_modificados': usuarios_modificados,
        'usuarios_admin': usuarios_admin,
        'usuarios_some': usuarios_some,
        'usuarios_matrona': usuarios_matrona,
        'usuarios_supervisor': usuarios_supervisor,
        'usuarios_auditoria': usuarios_auditoria,
        'usuarios_roles_anio': usuarios_roles_anio,
        'modificaciones_roles_mes': modificaciones_roles_mes,
        'fecha_hoy': str(hoy),
    })


# API: Estadísticas para panel matrona (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_matrona(request):
    total_partos = Parto.objects.count()
    partos_activos = Parto.objects.filter(estado='activo').count()
    hoy = timezone.now().date()
    partos_hoy = Parto.objects.filter(fecha_ingreso__date=hoy).count()
    partos_mes = Parto.objects.filter(fecha_ingreso__year=hoy.year, fecha_ingreso__month=hoy.month).count()
    return JsonResponse({
        'total_partos': total_partos,
        'partos_activos': partos_activos,
        'partos_hoy': partos_hoy,
        'partos_mes': partos_mes,
    })


# API: Estadísticas para panel SOME (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_some(request):
    total_madres = Madre.objects.count()
    return JsonResponse({
        'total_madres': total_madres
    })


# API: Estadísticas para panel supervisor (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_supervisor(request):
    User = get_user_model()
    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    hoy = timezone.now().date()
    eventos_hoy = Auditoria.objects.filter(fecha_hora__date=hoy).count()
    return JsonResponse({
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'eventos_hoy': eventos_hoy,
    })


# API: Estadísticas para panel auditoría (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_auditoria(request):
    total_eventos = Auditoria.objects.count()
    hoy = timezone.now().date()
    hace_una_semana = hoy - timezone.timedelta(days=7)
    eventos_hoy = Auditoria.objects.filter(fecha_hora__date=hoy).count()
    eventos_mes = Auditoria.objects.filter(fecha_hora__year=hoy.year, fecha_hora__month=hoy.month).count()
    acciones_count = Auditoria.objects.values('accion_realizada').distinct().count()
    
    # Obtener los últimos 10 eventos
    ultimos_eventos = Auditoria.objects.all().order_by('-fecha_hora')[:10]
    eventos_serializado = [
        {
            'accion': evento.accion_realizada,
            'modelo': evento.modelo_afectado or 'Sistema',
            'usuario': evento.usuario.username if evento.usuario else 'Sistema',
            'fecha': evento.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
        }
        for evento in ultimos_eventos
    ]
    
    return JsonResponse({
        'total_eventos': total_eventos,
        'eventos_hoy': eventos_hoy,
        'eventos_mes': eventos_mes,
        'total_acciones': acciones_count,
        'eventos_semana': Auditoria.objects.filter(fecha_hora__date__gte=hace_una_semana).count(),
        'ultimos_eventos': eventos_serializado,
        'fecha_consulta': hoy.strftime('%Y-%m-%d %H:%M:%S')
    })


# Vista para crear un nuevo usuario
@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='CREATE',
                modelo_afectado='Usuario',
                registro_id=user.id,
                detalles_cambio=f"Usuario creado: {user.username} (RUT: {getattr(user, 'rut', '')})",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = CustomUserForm()
    return render(request, 'roles/form_usuarios.html', {'form': form})

# Vista para editar los datos de un usuario existente
@login_required
def editar_usuario(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    # ADMIN no puede editar SUPERADMIN ni superuser
    if getattr(request.user, 'role', None) == 'ADMIN' and (user.role == 'SUPERADMIN' or user.is_superuser):
        messages.error(request, 'No tienes permisos para modificar este usuario.')
        return redirect('lista_usuarios')
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            user_edit = form.save()
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='UPDATE',
                modelo_afectado='Usuario',
                registro_id=user_edit.id,
                detalles_cambio=f"Usuario editado: {user_edit.username} (RUT: {getattr(user_edit, 'rut', '')})",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'roles/form_usuarios.html', {'form': form})

# Vista para bloquear (desactivar) un usuario
@login_required
def bloquear_usuario(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    # ADMIN no puede bloquear/eliminar SUPERADMIN ni superuser
    if getattr(request.user, 'role', None) == 'ADMIN' and (user.role == 'SUPERADMIN' or user.is_superuser):
        messages.error(request, 'No tienes permisos para bloquear este usuario.')
        return redirect('lista_usuarios')
    if request.method == 'POST':
        user.is_active = False
        user.save()
        registrar_evento_auditoria(
            usuario=request.user,
            accion_realizada='USER_BLOCKED',
            modelo_afectado='Usuario',
            registro_id=user.id,
            detalles_cambio=f"Usuario bloqueado: {user.username} (RUT: {getattr(user, 'rut', '')})",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        messages.success(request, 'Usuario bloqueado correctamente.')
        return redirect('lista_usuarios')
    return render(request, 'roles/bloquear_usuario.html', {'user': user})

# Vista para mostrar página de acceso no autorizado
def no_autorizado(request):
    """
    Vista para mostrar página de acceso no autorizado.
    Esta vista se puede usar tanto para usuarios no autenticados
    como para demostrar las medidas de seguridad del sistema.
    """
    return render(request, 'roles/no_autorizado.html')