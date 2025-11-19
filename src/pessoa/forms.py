from django import forms
from django.core.exceptions import ValidationError

from .models import PessoaFisica, PessoaJuridica, PessoaFisica, Funcionario

class ClientePfForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = ['nome', 'cpf', 'telefone', 'email']

class ClientePjForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'

class FuncionarioForm(forms.ModelForm):
	class Meta:
		model = Funcionario
		fields = [
			'nome',
			'telefone',
			'email',
			'cpf',
			'foto',
			'salario',
			'data_admissao',
			'data_demissao',
			#'ativo',
			'gerente',
		]
		widgets = {
			'data_admissao': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
			'data_demissao': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
		}

		input_formats = {
			'data_admissao': ['%Y-%m-%d'],
			'data_demissao': ['%Y-%m-%d'],
		}

	def clean(self):
		cleaned_data = super().clean()
		admissao = cleaned_data.get('data_admissao')
		demissao = cleaned_data.get('data_demissao')

		if admissao and demissao and demissao < admissao:
			raise ValidationError("A data de demissão não pode ser anterior à data de admissão")

		# if demissao is None:
		# 	cleaned_data['ativo'] = True
		# else:
		# 	cleaned_data['ativo'] = False

		# return cleaned_data
