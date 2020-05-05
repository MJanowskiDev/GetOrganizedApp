from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login

from .forms import  UserCreateForm

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('home')
    template_name = 'authapp/signupuser.html'


class SiteLoginView(auth_views.LoginView):
    template_name = 'authapp/login.html'
    success_url = reverse_lazy("home")


class SiteLogoutView(auth_views.LogoutView):
    template_name = 'authapp/logout.html'