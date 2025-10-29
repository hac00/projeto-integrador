from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email')

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'email')


