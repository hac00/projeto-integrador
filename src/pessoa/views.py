from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.urls import reverse_lazy

from .models import Cliente, Funcionario
from .forms import ClienteForm, FuncionarioForm

# Template View
class ClienteView(TemplateView):
    template_name = 'clientes.html'

class FuncionarioView(TemplateView):
    template_name = 'funcionarios.html'

# CRUD Cliente
class ClienteCreateView(CreateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'cliente_form.html'
	success_url = reverse_lazy('clientes_listar')
    
class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes_listar.html'
    context_object_name = 'clientes'

class ClienteUpdateView(UpdateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'cliente_form.html'
	success_url = reverse_lazy('clientes_listar')

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
        
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente_deletar.html'
    success_url = reverse_lazy('clientes')

# CRUD Funcionario
class FuncionarioCreateView(CreateView):
	model = Funcionario
	form_class = FuncionarioForm
	template_name = 'funcionario_form.html'
	success_url = reverse_lazy('funcionario_listar')
    
class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'funcionarios_listar.html'
    context_object_name = 'funcionarios'

class FuncionarioUpdateView(UpdateView):
	model = Funcionario
	form_class = FuncionarioForm
	template_name = 'funcionario_form.html'
	success_url = reverse_lazy('funcionario_listar')
        
class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'funcionario_deletar.html'
    success_url = reverse_lazy('funcionarios')