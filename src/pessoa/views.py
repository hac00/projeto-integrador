from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Cliente
from .forms import ClienteForm

class ClienteCreateView(CreateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'cliente_form.html'
	success_url = reverse_lazy('cliente_adicionar')

class ClienteUpdateView(UpdateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'cliente_form.html'
	success_url = reverse_lazy('cliente_adicionar')

	def get_initial(self):
		initial = super().get_initial()
		cliente = self.get_object()
		if cliente.tipoCliente == 'PF' and cliente.pessoa_fisica:
			pf = cliente.pessoa_fisica
			initial.update({
				'nome': pf.nome,
				'telefone': pf.telefone,
				'email': pf.email,
				'cpf': pf.cpf,
				'tipoCliente': 'PF'
			})
		elif cliente.tipoCliente == 'PJ' and cliente.pessoa_juridica:
			pj = cliente.pessoa_juridica
			initial.update({
				'nome': pj.nome,
				'telefone': pj.telefone,
				'email': pj.email,
				'cnpj': pj.cnpj,
				'tipoCliente': 'PJ'
			})
		return initial
