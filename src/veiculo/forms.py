from django import forms
from .models import Veiculo
from django.forms import TextInput, Select

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor', 'tipo', 'proprietario']
        widgets = {
            'placa': TextInput(attrs={'class': 'form-control'}),
            'modelo': TextInput(attrs={'class': 'form-control'}),
            'cor': TextInput(attrs={'class': 'form-control'}),
            'tipo': Select(attrs={'class': 'form-select'}),
            'proprietario': Select(attrs={'class': 'form-select'}),
        }
