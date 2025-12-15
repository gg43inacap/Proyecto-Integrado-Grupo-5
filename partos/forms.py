from django import forms
from django.forms import modelformset_factory
from .models import Parto, RN
from gestion_some.models import Madre
# pylint: disable=no-member

class PartoForm(forms.ModelForm):
    class Meta:
        model = Parto
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control date-picker',
                'placeholder': 'Selecciona una fecha'
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control time-picker',
                'placeholder': 'Selecciona una hora'
            }),
            'madre': forms.Select(attrs={'class': 'form-select'}),
            'tipo_parto': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
    
    madre = forms.ModelChoiceField(
        queryset=Madre.objects.all(),
        label='Madre',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RNForm(forms.ModelForm):
    class Meta:
        model = RN
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control date-picker',
                'placeholder': 'Selecciona una fecha'
            }),
            'hora_nacimiento': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control time-picker',
                'placeholder': 'Selecciona una hora'
            }),
            'madre': forms.Select(attrs={
                'id': 'id_madre',
                'class': 'form-select',
                'onchange': 'filtrarPartos()'
            }),
            'parto_asociado': forms.Select(attrs={
                'id': 'id_parto_asociado',
                'class': 'form-select'
            }),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'peso_nacimiento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'talla': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'perimetro_cefalico': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'apgar_1min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'apgar_5min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'apgar_10min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
        }
    
    madre = forms.ModelChoiceField(
        queryset=Madre.objects.all(),
        label='Madre',
        widget=forms.Select(attrs={
            'id': 'id_madre',
            'class': 'form-select',
            'onchange': 'filtrarPartos()'
        })
    )
    
    parto_asociado = forms.ModelChoiceField(
        queryset=Parto.objects.filter(estado='activo'),
        label='Parto',
        widget=forms.Select(attrs={
            'id': 'id_parto_asociado',
            'class': 'form-select'
        })
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        # Si se pasa un parto asociado, filtrar la madre y el parto
        parto = initial.get('parto_asociado')
        madre = initial.get('madre')
        if parto:
            self.fields['parto_asociado'].queryset = Parto.objects.filter(id=parto.id, estado='activo')
        if madre:
            self.fields['madre'].queryset = Madre.objects.filter(id=madre.id)
            # Filtrar solo partos activos de esta madre
            self.fields['parto_asociado'].queryset = Parto.objects.filter(madre=madre, estado='activo')
        else:
            # Por defecto, mostrar solo partos activos
            self.fields['parto_asociado'].queryset = Parto.objects.filter(estado='activo')

# Formset para múltiples RN
RNFormSet = modelformset_factory(
    RN,
    form=RNForm,
    extra=2,  # Puedes ajustar el número de formularios extra
    can_delete=False
)
