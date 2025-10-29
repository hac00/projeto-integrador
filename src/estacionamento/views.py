from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Vaga, Movimentacao
from .forms import MovimentacaoEntradaForm
from django.utils import timezone

# --- Vagas ---

class VagaListView(ListView):
    model = Vaga
    template_name = "vagas.html"
    context_object_name = "vagas"

class VagaCreateView(CreateView):
    model = Vaga
    template_name = "vaga_form.html"
    fields = ['numero']
    success_url = reverse_lazy('vagas')

class VagaUpdateView(UpdateView):
    model = Vaga
    template_name = "vaga_form.html"
    fields = ['numero', 'ocupada']
    success_url = reverse_lazy('vagas')

class VagaDeleteView(DeleteView):
    model = Vaga
    template_name = "vaga_deletar.html"
    success_url = reverse_lazy('vagas')

# --- Movimentacoes ---

class MovimentacaoListView(ListView):
    model = Movimentacao
    template_name = "movimentacoes.html"
    context_object_name = "movimentacoes"

class MovimentacaoEntradaView(CreateView):
    model = Movimentacao
    form_class = MovimentacaoEntradaForm
    template_name = "movimentacao_form.html"
    success_url = reverse_lazy('movimentacoes')

    def form_valid(self, form):
        # Marca a vaga como ocupada
        response = super().form_valid(form)
        vaga = form.instance.vaga
        vaga.ocupada = True
        vaga.save()
        return response

class MovimentacaoSaidaView(UpdateView):
    model = Movimentacao
    fields = []  # nenhum campo editável
    template_name = "movimentacao_saida.html"
    success_url = reverse_lazy('movimentacoes')

    def form_valid(self, form):
        movimentacao = form.instance
        movimentacao.finalizar(tarifa_hora=10)  # tarifa fixa
        return super().form_valid(form)

class MovimentacaoDeleteView(DeleteView):
    model = Movimentacao
    template_name = "movimentacao_deletar.html"
    success_url = reverse_lazy('movimentacoes')
