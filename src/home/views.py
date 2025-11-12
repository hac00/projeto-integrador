from django.shortcuts import render
from django.contrib.auth.views import LoginView


def index(request):
    return render(request, 'index.html')

class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
