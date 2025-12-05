from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def dashboard(request):
    rol = request.user.role  # Este campo lo agregaste en tu modelo CustomUser
    if rol == 'SOME':
        return render(request, 'roles/panel_some.html')
    elif rol == 'MATRONA':
        return render(request, 'roles/panel_matrona.html')
    elif rol == 'SUPERVISOR':
        return render(request, 'roles/panel_supervisor.html')
    elif rol == 'AUDITORIA':
        return render(request, 'roles/panel_auditoria.html')
    elif rol == 'ADMIN':
        return render(request, 'roles/panel_admin.html')
    else:
        return render(request, 'roles/no_autorizado.html')