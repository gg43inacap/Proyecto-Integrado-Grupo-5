from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from roles.models import CustomUser

def login_view(request):
	if request.method == 'POST':
		login_type = request.POST.get('login_type', 'username')
		user_input = request.POST.get('username')
		password = request.POST.get('password')
		user = None
		if login_type == 'rut':
			try:
				user_obj = CustomUser.objects.get(rut=user_input)
				username = user_obj.username
			except CustomUser.DoesNotExist:
				username = None
		else:
			username = user_input
		if username:
			user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('inicio')
		else:
			messages.error(request, 'Usuario o contraseña incorrectos. Por favor intente nuevamente.')
	return render(request, 'login/login.html')
