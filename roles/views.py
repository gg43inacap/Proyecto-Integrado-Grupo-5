from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserForm
from django.contrib import messages

def dashboard(request):
    # Bypass login demo SIEMPRE si hay parámetro rol (prioridad máxima)
    rol_param = request.GET.get('rol')
    if rol_param:
        # Usar el primer superusuario para pruebas
        User = get_user_model()
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            request.user = superuser
            request.session['bypass_demo'] = True
        rol = rol_param
        # Mostrar el panel correspondiente al rol del parámetro
        if rol == 'ADMIN' or rol == 'SUPERADMIN':
            return render(request, 'roles/panel_ADMIN.html')
        elif rol == 'SOME':
            return render(request, 'roles/panel_some.html')
        elif rol == 'MATRONA':
            return render(request, 'roles/panel_matrona.html')
        elif rol == 'SUPERVISOR':
            return render(request, 'roles/panel_supervisor.html')
        elif rol == 'AUDITORIA':
            return render(request, 'roles/panel_auditoria.html')
        else:
            return render(request, 'roles/no_autorizado.html')
    # Si no es demo, flujo normal
    rol = getattr(request.user, 'role', None)
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
        return render(request, 'roles/no_autorizado.html')

def user_list(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'roles/user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('user_list')
    else:
        form = CustomUserForm()
    return render(request, 'roles/user_form.html', {'form': form})

@login_required
def user_update(request, pk):
    User = get_user_model()
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_list')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'roles/user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    User = get_user_model()
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('user_list')
    return render(request, 'roles/user_confirm_delete.html', {'user': user})