from django import forms
from django.forms import modelformset_factory
from .models import Parto, RN
from gestion_some.models import Madre
# pylint: disable=no-member

class PartoForm(forms.ModelForm):
    class Meta:
        model = Parto
        fields = '__all__'
    madre = forms.ModelChoiceField(queryset=Madre.objects.all(), label='Madre', widget=forms.Select)

class RNForm(forms.ModelForm):
    class Meta:
        model = RN
        fields = '__all__'
    madre = forms.ModelChoiceField(queryset=Madre.objects.all(), label='Madre', widget=forms.Select(attrs={'id': 'id_madre', 'onchange': 'filtrarPartos()'}))
    parto_asociado = forms.ModelChoiceField(queryset=Parto.objects.filter(estado='activo'), label='Parto', widget=forms.Select(attrs={'id': 'id_parto_asociado'}))

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
    extra=2, # Puedes ajustar el número de formularios extra
    can_delete=False
)
