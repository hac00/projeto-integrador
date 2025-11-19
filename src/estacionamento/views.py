import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import Vaga, Movimentacao, Valor, Pagamento
from .forms import MovimentacaoEntradaForm, ValorForm


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

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(MovimentacaoListView, self).get_queryset()
        if buscar:
            qs = qs.filter(status=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            lista = paginator.get_page(self.request.GET.get('page'))
            return lista
        else:
            return messages.info(self.request, 'Não existem movimentacoes cadastradas')

class MovimentacaoEntradaView(CreateView):
    model = Movimentacao
    form_class = MovimentacaoEntradaForm
    template_name = "movimentacao_form.html"
    success_url = reverse_lazy('movimentacoes')

    def form_valid(self, form):
        response = super().form_valid(form)
        vaga = form.instance.vaga
        vaga.ocupada = True
        vaga.save()
        return response

class MovimentacaoSaidaView(UpdateView):
    model = Movimentacao
    fields = []
    template_name = "movimentacao_saida.html"
    success_url = reverse_lazy('movimentacoes')

    def form_valid(self, form):
        movimentacao = form.instance
        tarifa = Valor.objects.first().valor_hora
        movimentacao.finalizar(tarifa)
        forma_pagamento = self.request.POST.get('forma_pagamento')
        valor_pagamento = movimentacao.valor
        from decimal import Decimal
        if forma_pagamento == 'PIX':
            valor_pagamento *=  Decimal(0.85)
        if forma_pagamento == 'DINHEIRO':
            valor_pagamento *= Decimal(0.90)
        Pagamento.objects.create(
            movimentacao=movimentacao,
            forma=forma_pagamento,
            valor=valor_pagamento
        )
        movimentacao.enviar_email()
        return super().form_valid(form)

class MovimentacaoFinalizarView(DetailView):
    model = Movimentacao
    template_name = 'movimentacao_saida.html'
    context_object_name = 'movimentacao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarifa = Valor.objects.first().valor_hora
        context['pagamento'] = self.object.calcular_valor(tarifa)
        context['tempo_estimado'] = self.object.tempo_permanencia()

        return context


class MovimentacaoDeleteView(DeleteView):
    model = Movimentacao
    template_name = "movimentacao_deletar.html"
    success_url = reverse_lazy('movimentacoes')

class ValorUpdateView(UpdateView):
    model = Valor
    form_class = ValorForm
    template_name = 'valor_form.html'
    success_url = reverse_lazy('movimentacoes')

    def get_object(self, queryset=None):
        obj, _ = Valor.objects.get_or_create(id=1) #retorna tupla (obj & boolean)
        return obj

class RelatorioMovimentacaoView(TemplateView):
    template_name = "relatorio_movimentacoes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        status = self.request.GET.get('status', 'finalizada')

        movimentacoes = Movimentacao.objects.filter(status=status)

        # if data_inicio:
        #     try:
        #         dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        #         movimentacoes = movimentacoes.filter(entrada__date__gte=dt_inicio)
        #     except ValueError:
        #         pass

        # if data_fim:
        #     try:
        #         dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        #         movimentacoes = movimentacoes.filter(entrada__date__lte=dt_fim)
        #     except ValueError:
        #         pass

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