from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)