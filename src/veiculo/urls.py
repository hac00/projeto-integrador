from django.urls import path
from .views import (
    VeiculoListView, VeiculoCreateView,
    VeiculoUpdateView, VeiculoDeleteView,
    VeiculoDetailView
)

urlpatterns = [
    path('veiculos/', VeiculoListView.as_view(), name='veiculos'),
    path('veiculos/adicionar/', VeiculoCreateView.as_view(), name='veiculo_adicionar'),
    path('veiculos/editar/<int:pk>/', VeiculoUpdateView.as_view(), name='veiculo_editar'),
    path('veiculos/deletar/<int:pk>/', VeiculoDeleteView.as_view(), name='veiculo_deletar'),
    path('veiculos/detalhe/<int:pk>/', VeiculoDetailView.as_view(), name='veiculo_detalhe'),
]
