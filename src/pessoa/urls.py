from django.urls import path

from .views import ClienteCreateView, ClienteUpdateView, ClienteListView, ClienteDeleteView, ClienteView

urlpatterns = [
	path('cliente/cadastrar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
	path('cliente/<int:pk>/atualizar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/listar/', ClienteListView.as_view(), name='clientes_listar'),
    path('cliente/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_deletar'),
    path('cliente/', ClienteView.as_view(), name='clientes')
]