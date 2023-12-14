from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView

from users.forms import RegisterForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('cinema:home_page')


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('cinema:home_page')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('cinema:home_page')
    login_url = reverse_lazy('users:login')
