from datetime import timedelta
from unittest.mock import MagicMock
from django.test import RequestFactory
from django.test import TestCase
from django.utils import timezone

from cinema.forms import PurchaseForm
from cinema.models import CinemaHall, MovieSession, Movie
from users.models import Customer


class PurchaseFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.hall = CinemaHall.objects.create(name='Hall 1', places=100)
        self.user = Customer.objects.create(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Movie 1')
        self.session = MovieSession.objects.create(
            hall=self.hall,
            price=10,
            movie=self.movie,
            time_start='12:00',
            time_end='14:00',
            date_start=timezone.now().date(),
            date_end=(timezone.now() + timedelta(days=1)).date(),
        )
        self.data = {'tickets': 5}

    def test_valid_form(self):
        request = self.factory.post('/purchase/', data=self.data)
        form = PurchaseForm(self.data, request=request, customer=self.user, session_id=self.movie.pk)
        self.assertTrue(form.is_valid())

    # def test_invalid_form(self):
    #     request = self.factory.post('/purchase/', data=self.data)
    #     self.data['tickets'] = 200
    #     form = PurchaseForm(self.data, request=request, customer=self.user, session_id=self.movie.pk)
    #     self.assertFalse(form.is_valid())
