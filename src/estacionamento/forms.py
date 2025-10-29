from django import forms
from .models import Vaga, Movimentacao

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['numero', 'ocupada']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'ocupada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MovimentacaoEntradaForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['veiculo', 'vaga', 'funcionario']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'vaga': forms.Select(attrs={'class': 'form-select'}),
            'funcionario': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        vaga = cleaned_data.get("vaga")
        if vaga and vaga.ocupada:
            raise forms.ValidationError("Essa vaga já está ocupada!")
        return cleaned_data
