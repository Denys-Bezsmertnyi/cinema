from django.utils import timezone
from rest_framework import serializers

from cinema.models import MovieSession


def validate_date_range(date_start, date_end):
    if date_start and date_end and date_start > date_end:
        raise serializers.ValidationError('Start date cannot be before end date')


def validate_time_range(time_start, time_end):
    if time_start and time_end and time_start >= time_end:
        raise serializers.ValidationError('Start time cannot be before end time.')


def validate_past_date(date_end):
    if date_end and date_end < timezone.now().date():
        raise serializers.ValidationError('You cannot arrange movie shows for the past')


def validate_collisions(self, hall, date_start, date_end, time_start):
    if all([hall, date_start, date_end, time_start]):
        previous_shows = MovieSession.objects.filter(hall=hall)
        if self.instance:
            previous_shows = previous_shows.exclude(pk=self.instance.pk)
        for show in previous_shows:
            if show.date_end > date_start and show.time_end > time_start:
                raise serializers.ValidationError('This show collides with another show in this hall.')
