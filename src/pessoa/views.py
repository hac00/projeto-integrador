from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy

from .models import Pessoa, PessoaFisica, PessoaJuridica, Funcionario
from .forms import PessoaFisicaForm, PessoaJuridicaForm, FuncionarioForm

'''
# Template View
class ClienteView(TemplateView):
    template_name = 'clientes.html'

class FuncionarioView(TemplateView):
    template_name = 'funcionarios.html'
'''
# CRUD Cliente
class PessoaFisicaCreateView(CreateView):
	model = PessoaFisica
	form_class = PessoaFisicaForm
	template_name = 'pessoa_fisica_form.html'
	success_url = reverse_lazy('pessoas')

class PessoaJuridicaCreateView(CreateView):
	model = PessoaJuridica
	form_class = PessoaJuridicaForm
	template_name = 'pessoa_juridica_form.html'
	success_url = reverse_lazy('pessoas')

class PessoaView(ListView):
	model = Pessoa
	template_name = 'pessoas.html'
	#success_url = reverse_lazy('pessoa_fisica_form')
	context_object_name = 'pessoas'

	def get_queryset(self):
		buscar = self.request.GET.get('buscar')
		qs = super(PessoaView, self).get_queryset()
		qs = qs.exclude(id__in=Funcionario.objects.values_list('id', flat=True))
		# if buscar:
		# 	return qs.filter(nome__icontains=buscar)
		return qs

class PessoaDetailView(DetailView):
	model = Pessoa
	# template_name = 'pessoa_detalhe.html'
	context_object_name = 'pessoa'

	def get_template_names(self):
		return ['pessoa_detalhe.html']

'''    
class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'clientes'

class ClienteListView(ListView):
	model = Cliente
	template_name = 'clientes.html'
	context_object_name = 'clientes'

	def get_queryset(self):
		buscar = self.request.GET.get('buscar')
		qs = super(ClienteListView, self).get_queryset()
		# if buscar:
		# 	return qs.filter(nome__icontains=buscar)
		return qs

class ClienteUpdateView(UpdateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'cliente_form.html'
	success_url = reverse_lazy('clientes')

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

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)		
        
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cliente_deletar.html'
    success_url = reverse_lazy('clientes')
'''
# CRUD Funcionario
class FuncionarioCreateView(CreateView):
	model = Funcionario
	form_class = FuncionarioForm
	template_name = 'funcionario_form.html'
	success_url = reverse_lazy('funcionarios')

	def form_valid(self, form):
		funcionario = form.save(commit=False)
		if not funcionario.data_demissao:
			funcionario.ativo = True
		else:
			funcionario.ativo = False
		funcionario.save()
		return super().form_valid(form)	
    
class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'
    context_object_name = 'funcionarios'

class FuncionarioUpdateView(UpdateView):
	model = Funcionario
	form_class = FuncionarioForm
	template_name = 'funcionario_form.html'
	success_url = reverse_lazy('funcionarios')
        
class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'funcionario_deletar.html'
    success_url = reverse_lazy('funcionarios')

class FuncionarioDetailView(DetailView):
	model = Funcionario
	template_name = 'funcionario_detalhe.html'
	context_object_name = 'funcionario'
