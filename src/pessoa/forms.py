from django import forms

from .models import PessoaFisica, PessoaJuridica, Cliente

class ClienteForm(forms.ModelForm):
	tipoCliente = forms.ChoiceField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], label='Tipo de Cliente')
	nome = forms.CharField(label='Nome completo da pessoa ou empresa', max_length=100)
	telefone = forms.CharField(label='Telefone', max_length=15)
	email = forms.EmailField(label='E-mail')
	cpf = forms.CharField(label='CPF', max_length=14, required=False)
	cnpj = forms.CharField(label='CNPJ', max_length=14, required=False)

	class Meta:
		model = Cliente
		fields = ['tipoCliente']

	def save(self, commit=True):
		tipoCliente = self.cleaned_data['tipoCliente']
		nome = self.cleaned_data['nome']
		telefone = self.cleaned_data['telefone']
		email = self.cleaned_data['email']

		if tipoCliente == 'PF':
			pessoa = PessoaFisica(
				nome=nome,
				telefone=telefone,
				email=email,
				cpf=self.cleaned_data['cpf']
			)
			pessoa.save()
			cliente = Cliente(tipoCliente=tipoCliente, pessoa_fisica=pessoa)
		else:
			pessoa = PessoaJuridica(
			    nome=nome,
			    telefone=telefone,
			    email=email,
			    cnpj=self.cleaned_data['cnpj']
			)
			pessoa.save()
			cliente = Cliente(tipoCliente=tipoCliente, pessoa_juridica=pessoa)

		if commit:
		    cliente.save()

		return cliente
