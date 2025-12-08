from django.contrib.auth.decorators import login_required # Requiere que el usuario esté autenticado
from django.shortcuts import render, redirect # Mostrar páginas y redirigir
from django.contrib.auth import get_user_model # Obtener el modelo de usuario personalizado
from .forms import CustomUserForm # Importa el formulario para usuarios

from django.contrib import messages # Importa el sistema de mensajes para mostrar avisos
from auditoria.models import registrar_evento_auditoria

# Vista principal que muestra el panel según el rol del usuario
# Si se pasa el parámetro 'rol', muestra el panel de ese rol para pruebas
# Si no, muestra el panel según el rol del usuario logueado

@login_required
def dashboard(request): # Muestra el panel correspondiente al rol
    # Verificación de seguridad: solo usuarios autenticados con rol válido
    if not request.user.is_authenticated:
        return render(request, 'roles/no_autorizado.html')
    
    rol_param = request.GET.get('rol') # Obtiene el parámetro de rol si existe
    if rol_param:
        # Solo superuser puede usar modo demo
        if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'SUPERADMIN'):
            messages.error(request, 'No tiene permisos para acceder al modo demo.')
            return render(request, 'roles/no_autorizado.html')
        
        User = get_user_model() # Obtiene el modelo de usuario
        superuser = User.objects.filter(is_superuser=True).first() # Busca el primer superusuario
        if superuser:
            request.user = superuser # Asigna el superusuario para pruebas
            request.session['bypass_demo'] = True # Marca la sesión como demo
        rol = rol_param # Usa el rol del parámetro
        # Muestra el panel según el rol
        if rol == 'ADMIN' or rol == 'SUPERADMIN':
            return render(request, 'roles/panel_admin.html') # Panel de admin
        elif rol == 'SOME':
            return render(request, 'roles/panel_some.html') # Panel de SOME
        elif rol == 'MATRONA':
            return render(request, 'roles/panel_matrona.html') # Panel de matrona
        elif rol == 'SUPERVISOR':
            return render(request, 'roles/panel_supervisor.html') # Panel de supervisor
        elif rol == 'AUDITORIA':
            return render(request, 'roles/panel_auditoria.html') # Panel de auditoria
        else:
            return render(request, 'roles/no_autorizado.html') # Panel de no autorizado
    # Si no es demo, flujo normal - verificar rol del usuario autenticado
    rol = getattr(request.user, 'role', None) # Obtiene el rol del usuario
    
    # Verificación adicional de seguridad
    if not rol or rol == '':
        messages.error(request, 'Usuario sin rol asignado. Contacte al administrador.')
        return render(request, 'roles/no_autorizado.html')
    
    # Renderizar panel según rol verificado
    if rol == 'SUPERADMIN':
        return render(request, 'roles/panel_admin.html', {'user_role_display': 'Super Administrador'})
    elif rol == 'SOME':
        return render(request, 'roles/panel_some.html', {'user_role_display': 'SOME'})
    elif rol == 'MATRONA':
        return render(request, 'roles/panel_matrona.html', {'user_role_display': 'Matrona'})
    elif rol == 'SUPERVISOR':
        return render(request, 'roles/panel_supervisor.html', {'user_role_display': 'Supervisor'})
    elif rol == 'AUDITORIA':
        return render(request, 'roles/panel_auditoria.html', {'user_role_display': 'Auditoría'})
    elif rol == 'ADMIN':
        return render(request, 'roles/panel_admin.html', {'user_role_display': 'Administrador'})
    else:
        messages.error(request, f'Rol no reconocido: {rol}. Acceso denegado.')
        return render(request, 'roles/no_autorizado.html') # Si no tiene rol válido

@login_required
# Vista para listar todos los usuarios registrados

def listar_usuario(request): # Lista todos los usuarios
    User = get_user_model() # Obtiene el modelo de usuario
    
    # Solo superuser puede ver otros superuser y SUPERADMIN
    if request.user.is_superuser:
        users = User.objects.all()
    else:
        # Ocultar SUPERADMIN y superuser para todos los demás (incluye ADMIN y AUDITORIA)
        users = User.objects.exclude(role='SUPERADMIN').exclude(is_superuser=True)
    return render(request, 'roles/lista_usuarios.html', {'users': users})

@login_required
# Vista para crear un nuevo usuario

def crear_usuario(request): # Crea un nuevo usuario
    if request.method == 'POST': # Si el formulario fue enviado
        form = CustomUserForm(request.POST) # Crea el formulario con los datos enviados
        if form.is_valid(): # Si el formulario es válido
            user = form.save() # Guarda el usuario
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='CREATE',
                modelo_afectado='Usuario',
                registro_id=user.id,
                detalles_cambio=f"Usuario creado: {user.username} (RUT: {getattr(user, 'rut', '')})",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Usuario creado correctamente.') # Muestra mensaje de éxito
            return redirect('lista_usuarios') # Redirige a la lista de usuarios
    else:
        form = CustomUserForm() # Crea un formulario vacío
    return render(request, 'roles/form_usuarios.html', {'form': form}) # Muestra el formulario de creación

@login_required
# Vista para editar los datos de un usuario existente

def editar_usuario(request, pk): # Edita un usuario
    User = get_user_model() # Obtiene el modelo de usuario
    
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('lista_usuarios')
    
    # Solo superuser puede editar SUPERADMIN o otros superuser
    if not request.user.is_superuser and (user.role == 'SUPERADMIN' or user.is_superuser):
        messages.error(request, 'No tienes permisos para modificar este usuario.')
        return redirect('lista_usuarios')
    if request.method == 'POST': # Si el formulario fue enviado
        form = CustomUserForm(request.POST, instance=user) # Crea el formulario con los datos enviados
        if form.is_valid(): # Si el formulario es válido
            user_edit = form.save() # Guarda los cambios
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='UPDATE',
                modelo_afectado='Usuario',
                registro_id=user_edit.id,
                detalles_cambio=f"Usuario editado: {user_edit.username} (RUT: {getattr(user_edit, 'rut', '')})",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Usuario actualizado correctamente.') # Muestra mensaje de éxito
            return redirect('lista_usuarios') # Redirige a la lista de usuarios
    else:
        form = CustomUserForm(instance=user) # Crea el formulario con los datos actuales
    return render(request, 'roles/form_usuarios.html', {'form': form}) # Muestra el formulario de edición

@login_required
# Vista para eliminar un usuario

def bloquear_usuario(request, pk): # Elimina un usuario
    User = get_user_model() # Obtiene el modelo de usuario
    
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('lista_usuarios')
    
    # Solo superuser puede bloquear SUPERADMIN o otros superuser
    if not request.user.is_superuser and (user.role == 'SUPERADMIN' or user.is_superuser):
        messages.error(request, 'No tienes permisos para bloquear este usuario.')
        return redirect('lista_usuarios')
    if request.method == 'POST':
        user.is_active = False  # Solo bloquea el usuario
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

def no_autorizado(request):
    """
    Vista para mostrar página de acceso no autorizado.
    Esta vista se puede usar tanto para usuarios no autenticados
    como para demostrar las medidas de seguridad del sistema.
    """
    return render(request, 'roles/no_autorizado.html')