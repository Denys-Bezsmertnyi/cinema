from django.contrib import admin

from cinema.models import CinemaHall, Movie, MovieSession, Purchase

admin.site.register(CinemaHall)
admin.site.register(Movie)
admin.site.register(MovieSession)
admin.site.register(Purchase)
