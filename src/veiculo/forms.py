from django import forms
from .models import Veiculo
from django.forms import TextInput, Select
from pessoa.models import Pessoa, Funcionario

class VeiculoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VeiculoForm, self).__init__(*args, **kwargs)
        self.fields['proprietario'].queryset = Pessoa.objects.all().exclude(id__in=Funcionario.objects.all())

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
