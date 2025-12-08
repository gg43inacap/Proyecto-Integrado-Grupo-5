from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from auditoria.models import registrar_evento_auditoria

def inicio(request):
    return render(request, 'inicio.html')

def logout_view(request):
    """Vista personalizada para logout que acepta GET y POST"""
    if request.user.is_authenticated:
        user = request.user
        
        # Registrar logout en auditoría antes de cerrar sesión
        registrar_evento_auditoria(
            usuario=user,
            accion_realizada='LOGOUT',
            modelo_afectado='Usuario',
            registro_id=user.id,
            detalles_cambio=f'Usuario {user.username} ({user.role if hasattr(user, "role") else "Sin rol"}) cerró sesión',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        logout(request)
        messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('inicio')