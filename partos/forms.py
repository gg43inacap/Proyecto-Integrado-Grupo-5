from django import forms # Sistema de formularios de Django
from .models import Parto, RN # Importa los modelos Parto y RN
from gestion_some.models import Madre
# pylint: disable=no-member

class PartoForm(forms.ModelForm): # Formulario para crear y editar partos
    class Meta:
        model = Parto # El formulario se basa en el modelo Parto
        fields = '__all__' # Incluye todos los campos del modelo
    madre = forms.ModelChoiceField(queryset=Madre.objects.all(), label='Madre', widget=forms.Select)

class RNForm(forms.ModelForm): # Formulario para crear y editar recién nacidos
    class Meta:
        model = RN # El formulario se basa en el modelo RN
        fields = '__all__' # Incluye todos los campos del modelo
    madre = forms.ModelChoiceField(queryset=Madre.objects.all(), label='Madre', widget=forms.Select)
    parto_asociado = forms.ModelChoiceField(queryset=Parto.objects.all(), label='Parto', widget=forms.Select)
