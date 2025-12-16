from django import forms
from .models import Madre


class MadreForm(forms.ModelForm):
    class Meta:
        model = Madre
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control calendario-amigable',
                'placeholder': 'DD/MM/AAAA',
                'autocomplete': 'off'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle y número'
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Los Puelches'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +56912345678'
            }),
            'cesfam': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Centro de Salud'
            }),
            'prevision': forms.Select(attrs={
                'class': 'form-select'
            }),
            'migrante': forms.Select(attrs={
                'class': 'form-select',
                'choices': [(True, 'Sí'), (False, 'No')]
            }),
            'pueblo_originario': forms.Select(attrs={
                'class': 'form-select',
                'choices': [(True, 'Sí'), (False, 'No')]
            }),
            'antecedentes_obstetricos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa los antecedentes obstétricos'
            }),
            'alergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'alergias_si': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Especifique las alergias'
            }),
        }
