from django.urls import path

from .views import ClienteCreateView, ClienteUpdateView

urlpatterns = [
	path('cliente/cadastrar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
	path('cliente/<int:pk>/atualizar/', ClienteUpdateView.as_view(), name='cliente_editar'),
]