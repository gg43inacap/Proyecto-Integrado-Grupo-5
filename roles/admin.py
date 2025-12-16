from django.contrib import admin  # Importa el sistema de administración de Django
from django.contrib.auth.admin import UserAdmin  # Importa la administración personalizada de usuarios
from .models import CustomUser  # Importa el modelo de usuario personalizado

class CustomUserAdmin(UserAdmin):  # Clase para personalizar la administración de usuarios en el panel de Django
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('role',)}),  # Agrega el campo 'role' al panel de administración
    )
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')  # Muestra estos campos en la lista de usuarios

admin.site.register(CustomUser, CustomUserAdmin)  # Registra el modelo CustomUser con la configuración personalizada