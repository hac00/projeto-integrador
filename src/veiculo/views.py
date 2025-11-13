from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Veiculo
from .forms import VeiculoForm

class VeiculoListView(ListView):
    model = Veiculo
    template_name = 'veiculos.html'
    context_object_name = 'veiculos'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VeiculoListView, self).get_queryset()
        if buscar:
            return qs.filter(placa__icontains=buscar)
        #return qs

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            lista = paginator.get_page(self.request.GET.get('page'))
            return lista
        else:
            return messages.info(self.request, 'Não existem veículos cadastrados')

class VeiculoCreateView(CreateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')

class VeiculoUpdateView(UpdateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculo_form.html'
    success_url = reverse_lazy('veiculos')

class VeiculoDeleteView(DeleteView):
    model = Veiculo
    template_name = 'veiculo_deletar.html'
    success_url = reverse_lazy('veiculos')

class VeiculoDetailView(DetailView):
    model = Veiculo
    template_name = 'veiculo_detalhe.html'
    context_object_name = 'veiculo'
