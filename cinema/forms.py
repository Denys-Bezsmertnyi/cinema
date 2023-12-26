from django import forms
from django.contrib import messages

from django.core.exceptions import ValidationError
from django.utils import timezone

from cinema.models import CinemaHall, MovieSession, Purchase


class HallCreationForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class SessionCreateAndUpdateForm(forms.ModelForm):
    class Meta:
        model = MovieSession
        fields = ['hall', 'price', 'movie', 'time_start', 'time_end', 'date_start', 'date_end']

        widgets = {
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'type': 'time'}),
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get('date_start')
        date_end = cleaned_data.get('date_end')
        time_start = cleaned_data.get('time_start')
        time_end = cleaned_data.get('time_end')

        if date_start and date_end and time_start and time_end:
            overlapping_sessions = MovieSession.objects.filter(
                hall=cleaned_data.get('hall'),
                date_start__lte=date_end,
                date_end__gte=date_start,
                time_start__lte=time_end,
                time_end__gte=time_start
            )
            if time_start >= time_end:
                self.add_error("time_end", "End time should be greater than start time")

            if self.instance and self.instance.pk:
                overlapping_sessions = overlapping_sessions.exclude(pk=self.instance.pk)

            if overlapping_sessions.exists():
                raise ValidationError("Do you wanna create a session in the hall that already has a session, omg :(")

        if (date_start > date_end) or ((date_start == date_end) and (time_start >= time_end)) \
                or date_end < timezone.now().date():
            self.add_error("__all__", "Incorrect date")


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['tickets']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.customer = kwargs.pop('customer', None)
        self.session_id = kwargs.pop('session_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            session = MovieSession.objects.get(pk=self.session_id)
            tickets = cleaned_data.get('tickets')
            available_places = session.hall.places - session.bought_places

            if tickets < 1:
                self.add_error('tickets',
                               'Zero tickets.')
                messages.error(self.request,
                               'Please choose at least one ticket.')

            if session and tickets:
                if tickets > session.hall.places:
                    self.add_error('tickets',
                                   'Many tickets.')
                    messages.error(self.request,
                                   'You specified more tickets than available in the hall.')

                elif tickets > available_places:
                    self.add_error('tickets',
                                   'Ticket unavailable.')
                    messages.error(self.request,
                                   'You specified more tickets than available for this session.')

                if self.customer.money < tickets * session.price:
                    self.add_error(None,
                                   'Insufficient balance.')
                    messages.error(self.request,
                                   'Sorry, it seems you do not have enough funds to complete this transaction.')

        except MovieSession.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request,
                           'Session does not exist.')
