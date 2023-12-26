from django.test import TestCase, Client
from django.urls import reverse_lazy
from cinema.models import CinemaHall
from cinema.views import HallCreateView
from cinema.forms import HallCreationForm


class HallCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_success_url(self):
        hall_data = {
            'name': 'Test Hall',
            'places': 100,
            'overview': 'Privet sladkiy',
        }

        form = HallCreationForm(hall_data)
        self.assertTrue(form.is_valid())

        created_hall = form.save()

        self.assertEqual(CinemaHall.objects.count(), 1)

        view = HallCreateView()
        view.object = created_hall

        success_url = view.get_success_url()

        expected_url = reverse_lazy('cinema:hall', kwargs={'hall_id': created_hall.pk})
        self.assertEqual(success_url, expected_url)
