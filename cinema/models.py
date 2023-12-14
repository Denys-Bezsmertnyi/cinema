from datetime import timedelta

from django.db import models
from django.urls import reverse

from users.models import Customer


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    places = models.PositiveIntegerField(default=1)
    overview = models.TextField(default='Common Hall')

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField(default=timedelta(minutes=0))
    release_year = models.IntegerField(default=2023)
    genre = models.CharField(max_length=255, default='Unknown')
    image = models.ImageField(upload_to='movie_images/', default='static/img/movie_default.jpg')

    def __str__(self):
        return f"{self.title} ({self.release_year}) - {self.duration} - {self.genre}"


class MovieSession(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='sessions')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    date_start = models.DateField()
    date_end = models.DateField()
    bought_places = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Session with id#{self.id} at {self.time_start}'

    def get_absolute_url(self):
        return reverse('cinema:session', args=[str(self.pk)])


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    session = models.ForeignKey(MovieSession, on_delete=models.CASCADE, related_name="purchases")
    purchase_time = models.DateTimeField(auto_now_add=True)
    tickets = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
