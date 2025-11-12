from django.db import models

from stdimage import StdImageField

class Pessoa(models.Model):
	nome = models.CharField('Nome', max_length=100, help_text='Nome completo')
	telefone = models.CharField('Telefone', max_length=15, help_text='Número de telefone')
	email = models.EmailField('E-mail', max_length=100, help_text='Endereço de e-mail')
	data_cadastro = models.DateField(auto_now_add=True)

	class Meta:
		abstract = False

	def __str__(self):
		return self.nome

class PessoaFisica(Pessoa):
	cpf = models.CharField('Cpf', max_length=14, help_text='Cpf da pessoa', unique=True)

	def __str__(self):
		return f'{self.nome} - CPF: {self.cpf}'

class PessoaJuridica(Pessoa):
	cnpj = models.CharField('Cnpj', max_length=14, help_text='Cnpj da empresa')

	def __str__(self):
		return f'{self.nome} - CNPJ: {self.cnpj}'

class Funcionario(PessoaFisica):
	foto = StdImageField('Foto', upload_to='media/funcionarios', null=True, blank=True)
	salario = models.DecimalField('Salário', max_digits=10, decimal_places=2)
	data_admissao = models.DateField('Data de admissão')
	data_demissao = models.DateField('Data de demissão', null=True, blank=True)
	ativo = models.BooleanField('Ativo', default=True)
	gerente = models.BooleanField('Gerente', default=False)

	class Meta:
		verbose_name = 'Funcionário'
		verbose_name_plural = 'Funcionários'

	def __str__(self):
		cargo = 'Gerente' if self.gerente else 'Funcionário'
		return f'{self.nome} - {cargo}'

	##funcionalidade: define "ativo" com base em data admissao e demissao
	#opt1
	def save(self, *args, **kwargs):
		if self.data_demissao:
			self.ativo = False
		else:
			self.ativo = True
		super().save(*args, **kwargs)

	#opt2
	'''
	def save(self, *args, **kwargs):
		self.ativo = not bool(self.data_demissao)
		super().save(*args, **kwargs)
	'''
	#opt3
	'''
	def save(self, *args, **kwargs):
		self.ativo = self.demissao is None
		super().save(*args, **kwargs)
	'''
	##