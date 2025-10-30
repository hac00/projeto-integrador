from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Veiculo
from .forms import VeiculoForm

class VeiculoListView(ListView):
    model = Veiculo
    template_name = 'veiculos.html'
    context_object_name = 'veiculos'

    # def get_queryset(self):
    #     queryset = Veiculo.objects.all()

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
