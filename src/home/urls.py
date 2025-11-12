from django.urls import path

from . import views
from .views import LoginView

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', LoginView.as_view(), name='login'),
]