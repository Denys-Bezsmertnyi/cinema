from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from cinema.models import CinemaHall
from cinema.views import HallCreateView


class HallCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin2', email='admin@example.com', password='adminpass'
        )
        self.url = reverse('cinema:create_hall')
        self.data = {
            'name': 'Test Hall',
            'places': 50,
            'overview': 'Test Hall Overview',
        }

    def test_view_with_valid_data(self):
        request = self.factory.post(self.url, self.data)
        request.user = self.admin_user

        response = HallCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)

        hall = CinemaHall.objects.last()
        self.assertEqual(hall.name, 'Test Hall')
        self.assertEqual(hall.places, 50)
        self.assertEqual(hall.overview, 'Test Hall Overview')

        self.assertEqual(response.url, reverse('cinema:hall', kwargs={'hall_id': hall.pk}))

    def test_view_with_invalid_data(self):
        invalid_data = {
            'name': '',
            'places': 50,
            'overview': 'Test Hall Overview',
        }

        request = self.factory.post(self.url, invalid_data)
        request.user = self.admin_user

        response = HallCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        halls_count = CinemaHall.objects.count()
        self.assertEqual(halls_count, 0)
