from django.urls import path

from . import views
from .views import LoginView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
]