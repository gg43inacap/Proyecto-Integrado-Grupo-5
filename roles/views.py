from django.contrib.auth.decorators import login_required # Requiere que el usuario esté autenticado
from django.shortcuts import render, redirect # Mostrar páginas y redirigir
from django.contrib.auth import get_user_model # Obtener el modelo de usuario personalizado
from .forms import CustomUserForm # Importa el formulario para usuarios
from django.contrib import messages # Importa el sistema de mensajes para mostrar avisos

# Vista principal que muestra el panel según el rol del usuario
# Si se pasa el parámetro 'rol', muestra el panel de ese rol para pruebas
# Si no, muestra el panel según el rol del usuario logueado

def dashboard(request): # Muestra el panel correspondiente al rol
    rol_param = request.GET.get('rol') # Obtiene el parámetro de rol si existe
    if rol_param:
        User = get_user_model() # Obtiene el modelo de usuario
        superuser = User.objects.filter(is_superuser=True).first() # Busca el primer superusuario
        if superuser:
            request.user = superuser # Asigna el superusuario para pruebas
            request.session['bypass_demo'] = True # Marca la sesión como demo
        rol = rol_param # Usa el rol del parámetro
        # Muestra el panel según el rol
        if rol == 'ADMIN' or rol == 'SUPERADMIN':
            return render(request, 'roles/panel_ADMIN.html') # Panel de admin
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
    # Si no es demo, flujo normal
    rol = getattr(request.user, 'role', None) # Obtiene el rol del usuario
    if rol == 'SUPERADMIN':
        return render(request, 'roles/panel_ADMIN.html')
    elif rol == 'SOME':
        return render(request, 'roles/panel_some.html')
    elif rol == 'MATRONA':
        return render(request, 'roles/panel_matrona.html')
    elif rol == 'SUPERVISOR':
        return render(request, 'roles/panel_supervisor.html')
    elif rol == 'AUDITORIA':
        return render(request, 'roles/panel_auditoria.html')
    elif rol == 'ADMIN':
        return render(request, 'roles/panel_ADMIN.html')
    else:
        return render(request, 'roles/no_autorizado.html') # Si no tiene rol válido

@login_required
# Vista para listar todos los usuarios registrados

def user_list(request): # Lista todos los usuarios
    User = get_user_model() # Obtiene el modelo de usuario
    users = User.objects.all() # Obtiene todos los usuarios
    return render(request, 'roles/user_list.html', {'users': users}) # Muestra la lista de usuarios

@login_required
# Vista para crear un nuevo usuario

def user_create(request): # Crea un nuevo usuario
    if request.method == 'POST': # Si el formulario fue enviado
        form = CustomUserForm(request.POST) # Crea el formulario con los datos enviados
        if form.is_valid(): # Si el formulario es válido
            form.save() # Guarda el usuario
            messages.success(request, 'Usuario creado correctamente.') # Muestra mensaje de éxito
            return redirect('user_list') # Redirige a la lista de usuarios
    else:
        form = CustomUserForm() # Crea un formulario vacío
    return render(request, 'roles/user_form.html', {'form': form}) # Muestra el formulario de creación

@login_required
# Vista para editar los datos de un usuario existente

def user_update(request, pk): # Edita un usuario
    User = get_user_model() # Obtiene el modelo de usuario
    user = User.objects.get(pk=pk) # Obtiene el usuario por su ID
    if request.method == 'POST': # Si el formulario fue enviado
        form = CustomUserForm(request.POST, instance=user) # Crea el formulario con los datos enviados
        if form.is_valid(): # Si el formulario es válido
            form.save() # Guarda los cambios
            messages.success(request, 'Usuario actualizado correctamente.') # Muestra mensaje de éxito
            return redirect('user_list') # Redirige a la lista de usuarios
    else:
        form = CustomUserForm(instance=user) # Crea el formulario con los datos actuales
    return render(request, 'roles/user_form.html', {'form': form}) # Muestra el formulario de edición

@login_required
# Vista para eliminar un usuario

def user_delete(request, pk): # Elimina un usuario
    User = get_user_model() # Obtiene el modelo de usuario
    user = User.objects.get(pk=pk) # Obtiene el usuario por su ID
    if request.method == 'POST': # Si se confirma la eliminación
        user.delete() # Elimina el usuario
        messages.success(request, 'Usuario eliminado correctamente.') # Muestra mensaje de éxito
        return redirect('user_list') # Redirige a la lista de usuarios
    return render(request, 'roles/user_confirm_delete.html', {'user': user}) # Muestra la página de confirmación