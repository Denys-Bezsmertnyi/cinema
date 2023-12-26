from django.test import TestCase

from cinema.models import CinemaHall, Movie, MovieSession, Purchase
from users.models import Customer


class CinemaHallModelTest(TestCase):
    def setUp(self):
        self.hall = CinemaHall.objects.create(
            name='Test Hall',
            places=50,
            overview='Test Hall Overview'
        )

    def test_cinema_hall_creation(self):
        self.assertEqual(self.hall.name, 'Test Hall')
        self.assertEqual(self.hall.places, 50)
        self.assertEqual(self.hall.overview, 'Test Hall Overview')

    def test_cinema_hall_str_method(self):
        self.assertEqual(str(self.hall), 'Test Hall')


class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Movie Description',
            duration='02:00:00',
            release_year=2023,
            genre='Action',
            image='movie_images/test_image.jpg',
        )

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.description, 'Test Movie Description')
        self.assertEqual(self.movie.duration, '02:00:00')
        self.assertEqual(self.movie.release_year, 2023)
        self.assertEqual(self.movie.genre, 'Action')
        self.assertEqual(self.movie.image, 'movie_images/test_image.jpg')

    def test_movie_str_method(self):
        expected_str = "Test Movie (2023) - 02:00:00 - Action"
        self.assertEqual(str(self.movie), expected_str)


class MovieSessionModelTest(TestCase):
    def setUp(self):
        self.hall = CinemaHall.objects.create(
            name='Test Hall',
            places=50,
            overview='Test Hall Overview'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Movie Description',
            duration='02:00:00',
            release_year=2023,
            genre='Action',
            image='movie_images/test_image.jpg',
        )
        self.movie_session = MovieSession.objects.create(
            hall=self.hall,
            price=10.50,
            movie=self.movie,
            time_start='12:00:00',
            time_end='14:00:00',
            date_start='2023-01-01',
            date_end='2023-01-02',
            bought_places=25,
        )

    def test_movie_session_creation(self):
        self.assertEqual(self.movie_session.hall, self.hall)
        self.assertEqual(self.movie_session.price, 10.50)
        self.assertEqual(self.movie_session.movie, self.movie)
        self.assertEqual(self.movie_session.time_start, '12:00:00')
        self.assertEqual(self.movie_session.time_end, '14:00:00')
        self.assertEqual(self.movie_session.date_start, '2023-01-01')
        self.assertEqual(self.movie_session.date_end, '2023-01-02')
        self.assertEqual(self.movie_session.bought_places, 25)

    def test_movie_session_str_method(self):
        expected_str = f'Session with id#{self.movie_session.id} at 12:00:00'
        self.assertEqual(str(self.movie_session), expected_str)

    def test_movie_session_get_absolute_url(self):
        expected_url = f'/session/{self.movie_session.pk}/'
        self.assertEqual(self.movie_session.get_absolute_url(), expected_url)


class PurchaseModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            username='testuser',
            password='testpass'
        )
        self.hall = CinemaHall.objects.create(
            name='Test Hall',
            places=50,
            overview='Test Hall Overview'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Movie Description',
            duration='02:00:00',
            release_year=2023,
            genre='Action',
            image='movie_images/test_image.jpg',
        )
        self.movie_session = MovieSession.objects.create(
            hall=self.hall,
            price=10.50,
            movie=self.movie,
            time_start='12:00:00',
            time_end='14:00:00',
            date_start='2023-01-01',
            date_end='2023-01-02',
            bought_places=25,
        )
        self.purchase = Purchase.objects.create(
            customer=self.customer,
            session=self.movie_session,
            tickets=3,
            total_amount=31.50,
        )

    def test_purchase_creation(self):
        self.assertEqual(self.purchase.customer, self.customer)
        self.assertEqual(self.purchase.session, self.movie_session)
        self.assertEqual(self.purchase.tickets, 3)
        self.assertEqual(self.purchase.total_amount, 31.50)

    def test_purchase_purchase_time_auto_now_add(self):
        self.assertIsNotNone(self.purchase.purchase_time)
