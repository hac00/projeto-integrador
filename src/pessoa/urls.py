from django.urls import path

from .views import ClienteCreateView

urlpatterns = [
	path('cliente/cadastrar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
]