from django import forms # Sistema de formularios de Django
from .models import CustomUser # Importa el modelo de usuario personalizado

class CustomUserForm(forms.ModelForm): # Formulario para crear y editar usuarios
    class Meta:
        model = CustomUser # El formulario se basa en el modelo CustomUser
        fields = ['username', 'email', 'role', 'is_active', 'is_staff'] # Campos que aparecerán en el formulario
        widgets = {
            'role': forms.Select(), # El campo 'role' se muestra como menú desplegable
        }
