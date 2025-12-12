# Vista para listar todos los usuarios registrados
# Limpieza de imports y organización
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from partos.models import Parto
from auditoria.models import registrar_evento_auditoria
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
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

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
from django.contrib.auth.decorators import login_required # Requiere que el usuario esté autenticado
from django.shortcuts import render, redirect # Mostrar páginas y redirigir
from django.contrib.auth import get_user_model # Obtener el modelo de usuario personalizado
from .forms import CustomUserForm # Importa el formulario para usuarios
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from partos.models import Parto
from django.contrib import messages # Importa el sistema de mensajes para mostrar avisos
from auditoria.models import registrar_evento_auditoria


# API: Estadísticas para panel admin (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_admin(request):
    User = get_user_model()
    total_usuarios = User.objects.count()
    usuarios_bloqueados = User.objects.filter(is_active=False).count()
    hoy = timezone.now().date()
    # Aquí puedes agregar más estadísticas si lo deseas
    return JsonResponse({
        'total_usuarios': total_usuarios,
        'usuarios_bloqueados': usuarios_bloqueados,
        'fecha_hoy': str(hoy),
    })


# API: Estadísticas para panel matrona (solo datos, nunca renderiza paneles)
@login_required
def api_estadisticas_matrona(request):
    total_partos = Parto.objects.count()
    partos_activos = Parto.objects.filter(estado='activo').count()
    hoy = timezone.now().date()
    partos_hoy = Parto.objects.filter(fecha_hora__date=hoy).count()
    partos_mes = Parto.objects.filter(fecha_hora__year=hoy.year, fecha_hora__month=hoy.month).count()
    return JsonResponse({
        'total_partos': total_partos,
        'partos_activos': partos_activos,
        'partos_hoy': partos_hoy,
        'partos_mes': partos_mes,
    })

# ...existing code...

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
    user = User.objects.get(pk=pk)
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
    user = User.objects.get(pk=pk)
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