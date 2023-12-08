from django.db import models


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    places = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/', default='static/img/movie_default.jpg')

    def __str__(self):
        return self.title


class MovieSession(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='sessions')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    date_start = models.DateField()
    date_end = models.DateField()
