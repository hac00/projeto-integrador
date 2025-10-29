from django import forms
from django.core.exceptions import ValidationError

from .models import PessoaFisica, PessoaJuridica, PessoaFisica, Funcionario

class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = ['nome', 'cpf', 'telefone', 'email']

class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'



'''
class ClienteForm(forms.ModelForm):
    tipoCliente = forms.ChoiceField(
        choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')],
        label='Tipo de Cliente'
    )
    nome = forms.CharField(label='Nome completo da pessoa ou empresa', max_length=100)
    telefone = forms.CharField(label='Telefone', max_length=15)
    email = forms.EmailField(label='E-mail')
    cpf = forms.CharField(label='CPF', max_length=14, required=False)
    cnpj = forms.CharField(label='CNPJ', max_length=14, required=False)

    class Meta:
        model = Cliente
        fields = ['tipoCliente']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        tipo = self.cleaned_data.get('tipoCliente')
        if tipo == 'PF' and cpf:
            qs = PessoaFisica.objects.filter(cpf=cpf)
            if PessoaFisica.objects.filter(cpf=cpf).exists():
                raise ValidationError("Já existe um cliente cadastrado com esse CPF.")
        return cpf

    # Pessoa.objects.exclude(id__in(Funcionario.objects.values_list('id_cliente', flat=True))):
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        tipo = self.cleaned_data.get('tipoCliente')
        if tipo == 'PJ' and cnpj:
            if PessoaJuridica.objects.filter(cnpj=cnpj).exists():
                raise ValidationError("Já existe uma empresa cadastrada com esse CNPJ.")
        return cnpj

    def save(self, commit=True):
        tipoCliente = self.cleaned_data['tipoCliente']
        nome = self.cleaned_data['nome']
        telefone = self.cleaned_data['telefone']
        email = self.cleaned_data['email']

        # Pega a instância existente se houver (Update), senão None (Create)
        cliente = super().save(commit=False)

        if tipoCliente == 'PF':
            if cliente.pessoa_fisica:
                pessoa = cliente.pessoa_fisica
                pessoa.nome = nome
                pessoa.telefone = telefone
                pessoa.email = email
                pessoa.cpf = self.cleaned_data['cpf']
                if commit:
                    pessoa.save()
            else:
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
'''
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
			'data_admissao': forms.DateInput(attrs={'type':'date'}),
			'data_demissao': forms.DateInput(attrs={'type':'date'}),
		}

	def clean(self):
		cleaned_data = super().clean()
		admissao = cleaned_data.get('data_admissao')
		demissao = cleaned_data.get('data_demissao')

		if admissao and demissao and demissao < admissao:
			raise ValidationError("A data de demissão não pode ser anterior à data de admissão")

		if demissao is None:
			cleaned_data['ativo'] = True
		else:
			cleaned_data['ativo'] = False

		return cleaned_data
