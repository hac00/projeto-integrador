from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from pessoa.models import Funcionario, Pessoa
from veiculo.models import Veiculo
from estacionamento.models import Vaga, Valor


# def index(request):
#     return render(request, 'index.html')

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['qtd_clientes'] = Pessoa.objects.count() - Funcionario.objects.count()
        context['qtd_funcionarios'] = Funcionario.objects.count()
        context['qtd_veiculos'] = Veiculo.objects.count()
        context['qtd_vagas'] = Vaga.objects.count()
        context['valor'] = Valor.objects.first().valor_hora
        return context

class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


