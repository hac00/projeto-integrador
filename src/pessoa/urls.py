from django.urls import path

from .views import ClientePfCreateView, ClientePjCreateView, ClienteListView, ClienteDeleteView, ClienteDetailView, ClientePfUpdateView, ClientePjUpdateView
from .views import FuncionarioCreateView, FuncionarioUpdateView, FuncionarioListView, FuncionarioDeleteView, FuncionarioDetailView

urlpatterns = [
    path('clientepf/', ClientePfCreateView.as_view(), name='clientepf'),
    path('clientepj/', ClientePjCreateView.as_view(), name='clientepj'),
    path('cliente/', ClienteListView.as_view(), name='clientes'),
    path('clientepf/<int:pk>/atualizar', ClientePfUpdateView.as_view(), name='clientepf_atualizar'),
    path('clientepj/<int:pk>/atualizar', ClientePjUpdateView.as_view(), name='clientepj_atualizar'),
    path('cliente/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_deletar'),
    path('cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detalhe'),
    path('funcionario/cadastrar/', FuncionarioCreateView.as_view(), name='funcionario_adicionar'),
    path('funcionario/<int:pk>/atualizar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionarios/', FuncionarioListView.as_view(), name='funcionarios'),
    path('funcionario/<int:pk>/deletar/', FuncionarioDeleteView.as_view(), name='funcionario_deletar'),
    path('funcionario/<int:pk>/', FuncionarioDetailView.as_view(), name='funcionario_detalhe'),

]