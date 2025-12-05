from django import forms
from .models import Parto, RN
from gestion_some.models import Madre

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
