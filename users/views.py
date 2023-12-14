from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from cinema.models import Purchase
from users.forms import RegisterForm
from users.models import Customer


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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_purchases = Purchase.objects.filter(customer=self.object).aggregate(Sum('total_amount'))
        context['total_purchases'] = total_purchases['total_amount__sum'] if total_purchases['total_amount__sum'] else 0
        context['purchases'] = Purchase.objects.filter(customer=self.object).all()
        return context
