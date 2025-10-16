from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Cliente
from .forms import ClienteForm

class ClienteCreateView(CreateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'cliente_form.html'
	success_url = reverse_lazy('cliente_adicionar')