# src/estacionamento/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('vagas/', views.VagaListView.as_view(), name='vagas'),
    path('vagas/adicionar/', views.VagaCreateView.as_view(), name='vaga_adicionar'),
    path('vagas/<int:pk>/editar/', views.VagaUpdateView.as_view(), name='vaga_editar'),
    path('vagas/<int:pk>/deletar/', views.VagaDeleteView.as_view(), name='vaga_deletar'),
    path('movimentacoes/', views.MovimentacaoListView.as_view(), name='movimentacoes'),
    path('movimentacoes/entrada/', views.MovimentacaoEntradaView.as_view(), name='movimentacao_entrada'),
    path('movimentacoes/<int:pk>/saida/', views.MovimentacaoSaidaView.as_view(), name='movimentacao_saida'),
    path('movimentacoes/<int:pk>/deletar/', views.MovimentacaoDeleteView.as_view(), name='movimentacao_deletar'),
]
