from django.urls import path

from .views import ClienteCreateView, ClienteUpdateView, ClienteListView, ClienteDeleteView, ClienteView
from .views import FuncionarioCreateView, FuncionarioUpdateView, FuncionarioListView, FuncionarioDeleteView, FuncionarioView

urlpatterns = [
	path('cliente/cadastrar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
	path('cliente/<int:pk>/atualizar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/listar/', ClienteListView.as_view(), name='cliente_listar'),
    path('cliente/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_deletar'),
    path('cliente/', ClienteView.as_view(), name='clientes'),
    path('funcionario/cadastrar/', FuncionarioCreateView.as_view(), name='funcionario_adicionar'),
    path('funcionario/<int:pk>/atualizar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionario/listar/', FuncionarioListView.as_view(), name='funcionario_listar'),
    path('funcionario/<int:pk>/deletar/', FuncionarioDeleteView.as_view(), name='funcionario_deletar'),
    path('funcionario/', FuncionarioView.as_view(), name='funcionarios')
]