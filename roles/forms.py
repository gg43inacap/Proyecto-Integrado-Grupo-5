from django import forms # Sistema de formularios de Django
from .models import CustomUser # Importa el modelo de usuario personalizado
from .utils import validar_rut # Importa el validador de RUT

class CustomUserForm(forms.ModelForm): # Formulario para crear y editar usuarios
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text="Dejar vacío para mantener la contraseña actual (solo al editar)"
    )
    
    class Meta:
        model = CustomUser # El formulario se basa en el modelo CustomUser
        fields = ['rut', 'username', 'email', 'role', 'is_active', 'is_staff'] # Campos que aparecerán en el formulario
        widgets = {
            'role': forms.Select(), # El campo 'role' se muestra como menú desplegable
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9',
                'id': 'id_rut'
            }),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut and not validar_rut(rut):
            raise forms.ValidationError('RUT inválido. Verifique el formato y dígito verificador.')
        return rut
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
