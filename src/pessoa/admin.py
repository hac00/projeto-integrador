from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica, Cliente

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email')

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'email')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tipoCliente', 'pessoa_fisica', 'pessoa_juridica')
