from django.db.models import Sum
from rest_framework import serializers

from cinema.API.validations import validate_date_range, validate_time_range, validate_past_date, validate_collisions
from cinema.models import CinemaHall, MovieSession, Movie, Purchase
from users.models import Customer


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'duration', 'description', 'release_year']


class SessionReadSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovieSession
        fields = ['id', 'hall', 'price', 'movie', 'time_start', 'time_end', 'date_start', 'date_end', 'bought_places']


class SessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ['id', 'hall', 'movie', 'price', 'time_start', 'time_end', 'date_start', 'date_end', 'bought_places']

    def validate(self, data):
        date_start = data.get('date_start', self.instance.date_start if self.instance else None)
        date_end = data.get('date_end', self.instance.date_end if self.instance else None)
        time_start = data.get('time_start', self.instance.time_start if self.instance else None)
        time_end = data.get('time_end', self.instance.time_end if self.instance else None)
        hall = data.get('hall', self.instance.hall if self.instance else None)

        validate_date_range(date_start, date_end)
        validate_time_range(time_start, time_end)
        validate_past_date(date_end)
        if self.instance:
            if self.instance.bought_places > 0:
                raise serializers.ValidationError('You cannot delete or update a movie_show with sold seats.')
            validate_collisions(self, hall, date_start, date_end, time_start)
        return data


class HallReadSerializer(serializers.ModelSerializer):
    sessions = SessionReadSerializer(many=True, read_only=True)

    class Meta:
        model = CinemaHall
        fields = ['id', 'name', 'places', 'overview', 'sessions']


class HallWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ['id', 'name', 'places', 'overview']

    def validate(self, data):
        if any([session.bought_places > 0 for session in self.instance.sessions.all()]):
            raise serializers.ValidationError('You cannot modify a cinema hall with booked shows.')
        return data


class PurchaseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'customer', 'session', 'tickets', 'total_amount']
        read_only_fields = ['customer']


class PurchaseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'customer', 'session', 'purchase_time', 'tickets', 'total_amount']
        read_only_fields = ['customer', 'total_amount']

    def validate(self, data):
        session = data.get('session')
        tickets = data.get('tickets')
        available_places = session.hall.places - session.bought_places

        if tickets < 1:
            raise serializers.ValidationError('Please choose at least one ticket.')

        if session and tickets:
            if tickets > session.hall.places:
                raise serializers.ValidationError('You specified more tickets than available in the hall.')

            elif tickets > available_places:
                raise serializers.ValidationError('You specified more tickets than available for this session.')

            if self.context['request'].user.money < tickets * session.price:
                raise serializers.ValidationError('Sorry, it seems you do not have enough funds to complete this '
                                                  'transaction.')

        return data
