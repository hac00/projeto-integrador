import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Vaga, Movimentacao
from .forms import MovimentacaoEntradaForm


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

class RelatorioMovimentacaoView(TemplateView):
    template_name = "relatorio_movimentacoes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pegar filtros do GET (opcional)
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        status = self.request.GET.get('status', 'finalizada')

        movimentacoes = Movimentacao.objects.filter(status=status)

        if data_inicio:
            try:
                dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
                movimentacoes = movimentacoes.filter(entrada__date__gte=dt_inicio)
            except ValueError:
                pass

        if data_fim:
            try:
                dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')
                movimentacoes = movimentacoes.filter(entrada__date__lte=dt_fim)
            except ValueError:
                pass

        total_valor = sum([m.valor or 0 for m in movimentacoes])
        total_movimentacoes = movimentacoes.count()
        media_horas = 0
        if total_movimentacoes > 0:
            horas_totais = sum([
                ((m.saida - m.entrada).total_seconds() / 3600) if m.saida else 0
                for m in movimentacoes
            ])
            media_horas = horas_totais / total_movimentacoes

        context['movimentacoes'] = movimentacoes
        context['total_valor'] = total_valor
        context['total_movimentacoes'] = total_movimentacoes
        context['media_horas'] = round(media_horas, 2)
        context['data_inicio'] = data_inicio or ''
        context['data_fim'] = data_fim or ''
        context['status'] = status

        return context
