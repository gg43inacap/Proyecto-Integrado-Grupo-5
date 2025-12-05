from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'is_active', 'is_staff']
        widgets = {
            'role': forms.Select(choices=CustomUser._meta.get_field('role').choices),
        }
