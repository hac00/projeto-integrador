from django.urls import path

from .views import PessoaFisicaCreateView, PessoaJuridicaCreateView
from .views import PessoaView
from .views import FuncionarioCreateView, FuncionarioUpdateView, FuncionarioListView, FuncionarioDeleteView, FuncionarioDetailView, PessoaDetailView

urlpatterns = [
    path('pessoaf/', PessoaFisicaCreateView.as_view(), name='pessoaf'),
    path('pessoaj/', PessoaJuridicaCreateView.as_view(), name='pessoaj'),
    path('pessoas/', PessoaView.as_view(), name='pessoas'),
    path('funcionario/cadastrar/', FuncionarioCreateView.as_view(), name='funcionario_adicionar'),
    path('funcionario/<int:pk>/atualizar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionarios/', FuncionarioListView.as_view(), name='funcionarios'),
    path('funcionario/<int:pk>/deletar/', FuncionarioDeleteView.as_view(), name='funcionario_deletar'),
    path('funcionario/<int:pk>/', FuncionarioDetailView.as_view(), name='funcionario_detalhe'),
    path('pessoa/<int:pk>/', PessoaDetailView.as_view(), name='pessoa_detalhe'),
	# path('cliente/cadastrar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
	# path('cliente/<int:pk>/atualizar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    # path('clientes/', ClienteListView.as_view(), name='clientes'),
    # path('cliente/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_deletar'),

]