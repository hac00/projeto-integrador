from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy

from .models import Pessoa, PessoaFisica, PessoaJuridica, Funcionario
from .forms import ClientePfForm, ClientePjForm, FuncionarioForm

'''
# Template View
class ClienteView(TemplateView):
    template_name = 'clientes.html'

class FuncionarioView(TemplateView):
    template_name = 'funcionarios.html'
'''
# CRUD Cliente
class ClientePfCreateView(CreateView):
	model = PessoaFisica
	form_class = ClientePfForm
	template_name = 'cliente_pf_form.html'
	success_url = reverse_lazy('clientes')

class ClientePjCreateView(CreateView):
	model = PessoaJuridica
	form_class = ClientePjForm
	template_name = 'cliente_pj_form.html'
	success_url = reverse_lazy('clientes')

class ClientePfUpdateView(UpdateView):
	model = PessoaFisica
	form_class = ClientePfForm
	template_name = 'cliente_pf_form.html'
	success_url = reverse_lazy('clientes')

class ClientePjUpdateView(UpdateView):
	model = PessoaJuridica
	form_class = ClientePjForm
	template_name = 'cliente_pj_form.html'
	success_url = reverse_lazy('clientes')

class ClienteListView(ListView):
	model = Pessoa
	template_name = 'clientes.html'
	context_object_name = 'clientes'

	def get_queryset(self):
		buscar = self.request.GET.get('buscar')
		#qs = super(ClienteListView, self).get_queryset()
		#qs = qs.exclude(id__in=Funcionario.objects.values_list('id', flat=True))
		pf = PessoaFisica.objects.exclude(id__in=Funcionario.objects.values_list('id', flat=True))
		pj = PessoaJuridica.objects.all()
		if buscar:
			#return qs.filter(nome__icontains=buscar)
			pf = pf.filter(nome__icontains=buscar)
			pj = pj.filter(nome__icontains=buscar)
		#return qs
		from itertools import chain #chain une as duas tabelas pf & pj
		return list(chain(pf, pj))

class ClienteDetailView(DetailView):
	model = Pessoa
	template_name = 'cliente_detalhe.html'
	context_object_name = 'cliente'

	# def get_template_names(self):
	# 	return ['cliente_detalhe.html']

class ClienteDeleteView(DeleteView):
    model = Pessoa
    template_name = 'cliente_deletar.html'
    success_url = reverse_lazy('clientes')

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

	def get_queryset(self):
		buscar = self.request.GET.get('buscar')
		qs = super(FuncionarioListView, self).get_queryset()
		if buscar:
			return qs.filter(nome__icontains=buscar)
		return qs

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
