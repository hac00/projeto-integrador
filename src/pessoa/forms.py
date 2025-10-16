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

    # Pega a instância existente se houver (Update), senão None (Create)
		cliente = super().save(commit=False)

		if tipoCliente == 'PF':
			if cliente.pessoa_fisica:
	            # Update da PessoaFisica existente
				pessoa = cliente.pessoa_fisica
				pessoa.nome = nome
				pessoa.telefone = telefone
				pessoa.email = email
				pessoa.cpf = self.cleaned_data['cpf']
				if commit:
					pessoa.save()
			else:
	            # Create (somente se realmente não houver)
				pessoa = PessoaFisica(
					nome=nome,
					telefone=telefone,
					email=email,
					cpf=self.cleaned_data['cpf']
				)
				if commit:
					pessoa.save()
			cliente.pessoa_fisica = pessoa
			cliente.pessoa_juridica = None
		else:  # PJ
			if cliente.pessoa_juridica:
				pessoa = cliente.pessoa_juridica
				pessoa.nome = nome
				pessoa.telefone = telefone
				pessoa.email = email
				pessoa.cnpj = self.cleaned_data['cnpj']
				if commit:
					pessoa.save()
			else:
				pessoa = PessoaJuridica(
					nome=nome,
					telefone=telefone,
					email=email,
					cnpj=self.cleaned_data['cnpj']
				)
				if commit:
					pessoa.save()
			cliente.pessoa_juridica = pessoa
			cliente.pessoa_fisica = None

		if commit:
			cliente.save()

		return cliente

