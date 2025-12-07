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
    madre = forms.ModelChoiceField(queryset=Madre.objects.all(), label='Madre', widget=forms.Select)
    parto_asociado = forms.ModelChoiceField(queryset=Parto.objects.all(), label='Parto', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        # Si se pasa un parto asociado, filtrar la madre y el parto
        parto = initial.get('parto_asociado')
        madre = initial.get('madre')
        if parto:
            self.fields['parto_asociado'].queryset = Parto.objects.filter(id=parto.id)
        if madre:
            self.fields['madre'].queryset = Madre.objects.filter(id=madre.id)

# Formset para múltiples RN
RNFormSet = modelformset_factory(
    RN,
    form=RNForm,
    extra=2, # Puedes ajustar el número de formularios extra
    can_delete=False
)
