#!/usr/bin/env python
"""
Verificar usuario auditor_demo
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

from roles.models import CustomUser

user = CustomUser.objects.get(username='auditor_demo')
print(f'Usuario: {user.username}')
print(f'Activo: {user.is_active}')
print(f'Rol: {user.role}')
print(f'RUT: {user.rut}')
print(f'Password válida para demo2025: {user.check_password("demo2025")}')