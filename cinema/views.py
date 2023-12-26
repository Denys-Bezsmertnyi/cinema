from datetime import date, timedelta

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from . import exceptions
from .forms import HallCreationForm, SessionCreateAndUpdateForm, PurchaseForm
from .mixins import AdminRequiredMixin, HallAndSessionMixin
from .models import Movie, CinemaHall, MovieSession, Purchase


class MovieListView(ListView):
    model = Movie
    template_name = 'cinema/index.html'
    context_object_name = 'movies'
    paginate_by = 4
    ordering = ['-release_year']


class HallCreateView(AdminRequiredMixin, CreateView):
    form_class = HallCreationForm
    template_name = 'cinema/hall/create_hall.html'

    def get_success_url(self):
        messages.success(self.request, "Hall created successful!")
        return reverse_lazy('cinema:hall', kwargs={'hall_id': self.object.pk})


class HallUpdateView(AdminRequiredMixin, HallAndSessionMixin, UpdateView):
    model = CinemaHall
    pk_url_kwarg = 'hall_id'
    template_name = 'cinema/hall/update_hall.html'
    fields = ['name', 'places', 'overview']

    def get_success_url(self):
        messages.success(self.request, "Update successful!")
        return reverse_lazy('cinema:hall', kwargs={'hall_id': self.object.pk})


class HallDeleteView(AdminRequiredMixin, HallAndSessionMixin, DeleteView):
    model = CinemaHall
    success_url = reverse_lazy('cinema:hall_list')
    pk_url_kwarg = 'hall_id'
    login_url = reverse_lazy('users:user_login')
    template_name = 'cinema/hall/delete_hall.html'

    def get_success_url(self):
        messages.success(self.request, "Delete successful!")
        return reverse_lazy('cinema:hall_list')


class HallDetailView(DetailView):
    model = CinemaHall
    pk_url_kwarg = 'hall_id'
    template_name = 'cinema/hall/detail_hall.html'
    context_object_name = 'hall'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = self.object.sessions.all().order_by('-date_start')
        return context


class HallListView(ListView):
    model = CinemaHall
    template_name = 'cinema/hall/hall_list.html'
    paginate_by = 5
    context_object_name = 'halls'
    ordering = ['-name']


class SessionCreateView(AdminRequiredMixin, CreateView):
    model = MovieSession
    form_class = SessionCreateAndUpdateForm
    template_name = 'cinema/session/create_session.html'
    success_url = reverse_lazy('cinema:session_list')

    def form_valid(self, form):
        try:
            form.save()
        except exceptions.SessionCollisionError:
            messages.add_message(self.request, messages.ERROR, "Session collision exist with another one")
            return HttpResponseRedirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Session was created")
            return HttpResponseRedirect(self.success_url)


class SessionUpdateView(AdminRequiredMixin, HallAndSessionMixin, UpdateView):
    model = MovieSession
    pk_url_kwarg = 'session_id'
    template_name = 'cinema/session/update_session.html'
    form_class = SessionCreateAndUpdateForm

    def get_success_url(self):
        messages.success(self.request, "Update successful!")
        return reverse_lazy('cinema:session', kwargs={'session_id': self.object.pk})


class SessionDeleteView(AdminRequiredMixin, HallAndSessionMixin, DeleteView):
    model = MovieSession
    pk_url_kwarg = 'session_id'
    login_url = reverse_lazy('users:user_login')
    template_name = 'cinema/session/delete_session.html'

    def get_success_url(self):
        messages.success(self.request, "Delete successful!")
        return reverse_lazy('cinema:session_list')


class SessionDetailView(DetailView):
    model = MovieSession
    pk_url_kwarg = 'session_id'
    template_name = 'cinema/session/detail_session.html'
    context_object_name = 'session'
    extra_context = {'form': PurchaseForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_seats'] = self.object.hall.places - self.object.bought_places
        return context


class SessionListView(ListView):
    model = MovieSession
    template_name = 'cinema/session/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 10
    ordering = ['-date_start']

    def get_queryset(self):
        filter_type = self.request.GET.get('filter')
        queryset = MovieSession.objects.all()
        if filter_type == 'today':
            queryset = MovieSession.objects.filter(date_start__lte=date.today(), date_end__gte=date.today())
        elif filter_type == 'tomorrow':
            queryset = MovieSession.objects.filter(date_start__lte=date.today() + timedelta(days=1),
                                                   date_end__gte=date.today() + timedelta(days=1))
        elif filter_type == 'price':
            queryset = queryset.order_by('price')
        elif filter_type == 'time':
            queryset = queryset.order_by('time_start')

        return queryset


class PurchaseTicketView(CreateView):
    login_url = reverse_lazy('users:login')
    pk_url_kwarg = 'session_id'
    model = Purchase
    form_class = PurchaseForm
    http_method_names = ['get', 'post']

    def get_success_url(self):
        session = self.object.session
        return session.get_absolute_url()

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'session_id': self.kwargs['session_id'],
            'customer': self.request.user})
        return kwargs

    def form_valid(self, form):
        purchase = form.save(commit=False)
        session = MovieSession.objects.get(pk=form.session_id)
        session.bought_places += form.cleaned_data['tickets']

        purchase.session = session

        purchase.tickets = form.cleaned_data['tickets']
        price = purchase.session.price
        purchase.total_amount = purchase.tickets * price

        customer = form.customer
        purchase.customer = customer
        customer.money -= purchase.total_amount

        with transaction.atomic():
            purchase.save()
            customer.save()
            session.save()

        messages.success(self.request, "Purchase successful!")
        return super().form_valid(form=form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form data.")
        return HttpResponseRedirect(reverse_lazy('cinema:session', kwargs={'session_id': self.kwargs['session_id']}))
