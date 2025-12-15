from django import forms
from django.forms import modelformset_factory
from .models import Parto, RN
from gestion_some.models import Madre
# pylint: disable=no-member

class PartoCreateForm(forms.ModelForm):
    """Formulario para crear un parto nuevo (estado será 'activo' por defecto)"""
    class Meta:
        model = Parto
        fields = '__all__'
        exclude = ['estado']  # Estado será 'activo' por defecto del modelo
        widgets = {
            'fecha_ingreso': forms.TextInput(attrs={
                'class': 'form-control calendario-amigable',
                'placeholder': 'DD/MM/AAAA',
                'readonly': 'readonly'
            }),
            'hora_ingreso': forms.TextInput(attrs={
                'class': 'form-control horario-amigable',
                'placeholder': 'HH:MM',
                'readonly': 'readonly'
            }),
            'madre': forms.Select(attrs={'class': 'form-select'}),
            'tipo_parto': forms.Select(attrs={'class': 'form-select'}),
            'complicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nombre_acompanante': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    madre = forms.ModelChoiceField(
        queryset=Madre.objects.all(),
        label='Madre',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class PartoForm(forms.ModelForm):
    """Formulario para editar un parto existente (incluye campo estado)"""
    class Meta:
        model = Parto
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.TextInput(attrs={
                'class': 'form-control calendario-amigable',
                'placeholder': 'DD/MM/AAAA',
                'readonly': 'readonly'
            }),
            'hora_ingreso': forms.TextInput(attrs={
                'class': 'form-control horario-amigable',
                'placeholder': 'HH:MM',
                'readonly': 'readonly'
            }),
            'madre': forms.Select(attrs={'class': 'form-select'}),
            'tipo_parto': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'complicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nombre_acompanante': forms.TextInput(attrs={'class': 'form-control'}),
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
            'fecha_nacimiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DD/MM/AAAA'
            }),
            'hora_nacimiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'HH:MM'
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
            'apellido_paterno_rn': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', "min": '500',"max": '6000'}),
            'talla': forms.NumberInput(attrs={'class': 'form-control',"min": '20',"max": '65'}),
            'cc': forms.NumberInput(attrs={'class': 'form-control', "default":'20', 'step': '0.1', 'min': '20', 'max': '50'}),
            'semanas_gestacion': forms.NumberInput(attrs={'class': 'form-control', "min": '20',"max": '45'}),
            'dias_gestacion': forms.NumberInput(attrs={'class': 'form-control', "min": '0',"max": '6'}),
            'apgar_1': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'apgar_5': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'lactancia_antes_60': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profesional_vhb': forms.TextInput(attrs={'class': 'form-control'}),
            'reanimacion': forms.Select(attrs={'class': 'form-select'}),
            'ehi_grado': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_anomalia': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'fecha_nacimiento': 'Fecha de nacimiento',
            'hora_nacimiento': 'Hora de nacimiento',
            'madre': 'Madre',
            'parto_asociado': 'Parto asociado',
            'apellido_paterno_rn': 'Apellido paterno del RN',
            'sexo': 'Sexo',
            'peso': 'Peso (gramos)',
            'talla': 'Talla (cm)',
            'cc': 'Circunferencia craneana (cm)',
            'semanas_gestacion': 'Semanas de gestación',
            'dias_gestacion': 'Días de gestación',
            'apgar_1': 'APGAR al minuto 1',
            'apgar_5': 'APGAR a los 5 minutos',
            'profesional_vhb': 'Profesional que vacunó',
            'lactancia_antes_60': 'Lactancia antes de 60 minutos',
            'reanimacion': 'Reanimación',
            'ehi_grado': 'Grado EHI',
            'descripcion_anomalia': 'Descripción de anomalía',
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
