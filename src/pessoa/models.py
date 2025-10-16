from django.db import models

from stdimage import StdImageField

class Pessoa(models.Model):
	nome = models.CharField('Nome', max_length=100, help_text='Nome completo')
	telefone = models.CharField('Telefone', max_length=15, help_text='Número de telefone')
	email = models.EmailField('E-mail', max_length=100, help_text='Endereço de e-mail')
	data_cadastro = models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract = True

class PessoaFisica(Pessoa):
	cpf = models.CharField('Cpf', max_length=14, help_text='Cpf da pessoa')

	def __str__(self):
		return f'{self.nome} - CPF: {self.cpf}'

class PessoaJuridica(Pessoa):
	cnpj = models.CharField('Cnpj', max_length=14, help_text='Cnpj da empresa')

	def __str__(self):
		return f'{self.nome} - CNPJ: {self.cnpj}'

class Cliente(models.Model):
    TIPO_CHOICES = [('PF', 'Pessoa Física'),('PJ', 'Pessoa Juridica')]
    tipoCliente = models.CharField('Tipo', max_length=2, choices=TIPO_CHOICES)
    pessoa_fisica = models.OneToOneField(PessoaFisica, on_delete=models.CASCADE, null=True, blank=True, related_name='clientes_pf')
    pessoa_juridica = models.OneToOneField(PessoaJuridica, on_delete=models.CASCADE, null=True, blank=True, related_name='clientes_pj')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #ordering = [Upper('nome')] Como ordenar por nome?

    def __str__(self):
	    if self.tipoCliente == 'PF' and self.pessoa_fisica:
	        return self.pessoa_fisica.nome
	    elif self.tipoCliente == 'PJ' and self.pessoa_juridica:
	        return self.pessoa_juridica.nome
	    return 'Cliente sem pessoa vinculada'

class Funcionario(PessoaFisica):
	foto = StdImageField('Foto', upload_to='funcionarios/', null=True, blank=True)
	salario = models.DecimalField('Salário', max_digits=10, decimal_places=2)
	data_admissao = models.DateTimeField('Data de admissão')
	data_demissao = models.DateTimeField('Data de demissão', null=True, blank=True)
	ativo = models.BooleanField('Ativo', default=True)
	gerente = models.BooleanField('Gerente', default=False)

	class Meta:
		verbose_name = 'Funcionário'
		verbose_name_plural = 'Funcionários'

	def __str__(self):
		cargo = 'Gerente' if self.gerente else 'Funcionário'
		return f'{self.nome} - {cargo}'