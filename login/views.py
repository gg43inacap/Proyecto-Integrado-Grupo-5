
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from roles.models import CustomUser
from roles.utils import validar_rut
from auditoria.models import registrar_evento_auditoria
# pylint: disable=no-member
def login_view(request):
	if request.method == 'POST':
		login_type = request.POST.get('login_type', 'username')
		user_input = request.POST.get('username')
		password = request.POST.get('password')
		user = None
		username = None
		if login_type == 'rut':
			# Validar formato y dígito verificador antes de buscar usuario
			if not validar_rut(user_input):
				messages.error(request, 'RUT inválido. Por favor verifique el formato y dígito verificador.')
				return render(request, 'login/login.html')
			try:
				user_obj = CustomUser.objects.get(rut=user_input)
				username = user_obj.username
			except CustomUser.DoesNotExist:
				username = None
		else:
			# Solo modo usuario, nunca validar RUT
			username = user_input
		if username:
			user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			
			# Registrar login exitoso
			registrar_evento_auditoria(
				usuario=user,
				accion_realizada='LOGIN_SUCCESS',
				modelo_afectado='Usuario',
				registro_id=user.id,
				detalles_cambio=f'Usuario {user.username} ({user.role if hasattr(user, "role") else "Sin rol"}) inició sesión exitosamente',
				ip_address=request.META.get('REMOTE_ADDR')
			)
			
			# Solo superuser va al inicio (para activar demo), otros van directo a dashboard
			if user.is_superuser:
				return redirect('inicio')
			else:
				return redirect('dashboard')
		else:
			# Registrar intento de login fallido
			registrar_evento_auditoria(
				usuario=None,
				accion_realizada='LOGIN_FAILED',
				modelo_afectado='Usuario',
				registro_id=None,
				detalles_cambio=f'Intento de login fallido para usuario: {username or user_input}',
				ip_address=request.META.get('REMOTE_ADDR')
			)
			messages.error(request, 'Usuario o contraseña incorrectos. Por favor intente nuevamente.')
	return render(request, 'login/login.html')
