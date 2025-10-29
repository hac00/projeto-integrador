from django.urls import path

from .views import ClienteCreateView, ClienteUpdateView, ClienteListView, ClienteDeleteView
from .views import FuncionarioCreateView, FuncionarioUpdateView, FuncionarioListView, FuncionarioDeleteView

urlpatterns = [
	path('cliente/cadastrar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
	path('cliente/<int:pk>/atualizar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('cliente/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_deletar'),
    path('funcionario/cadastrar/', FuncionarioCreateView.as_view(), name='funcionario_adicionar'),
    path('funcionario/<int:pk>/atualizar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionarios/', FuncionarioListView.as_view(), name='funcionarios'),
    path('funcionario/<int:pk>/deletar/', FuncionarioDeleteView.as_view(), name='funcionario_deletar'),
]