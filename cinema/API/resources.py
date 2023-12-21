from datetime import timedelta, datetime

from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.API.mixins import CheckPurchasedTicketsMixin
from cinema.API.serializers import SessionReadSerializer, HallReadSerializer, MovieSerializer, SessionWriteSerializer, \
    HallWriteSerializer, PurchaseWriteSerializer, PurchaseReadSerializer
from cinema.models import CinemaHall, MovieSession, Movie, Purchase
from users.API.permissions import IsAdminOrReadOnly
from users.models import Customer


class HallViewSet(CheckPurchasedTicketsMixin, viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return HallWriteSerializer
        return HallReadSerializer


class SessionViewSet(CheckPurchasedTicketsMixin, viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return SessionWriteSerializer
        return SessionReadSerializer

    def get_queryset(self):
        queryset = MovieSession.objects.all()
        if self.request.method == 'GET':
            if self.request.query_params.get('day') == 'today':
                today = timezone.now().date()
                queryset = queryset.filter(
                    Q(date_start__lte=today, date_end__gte=today))
                from_time = self.request.query_params.get('from')
                to_time = self.request.query_params.get('to')
                hall = self.request.query_params.get('hall')
                if from_time and to_time:
                    from_time = datetime.strptime(from_time, "%H:%M").time()
                    to_time = datetime.strptime(to_time, "%H:%M").time()
                    queryset = queryset.filter(
                        Q(time_start__gte=from_time) & Q(time_start__lte=to_time)
                    )
                if hall:
                    queryset = queryset.filter(hall=hall).order_by('time_start')
            elif self.request.query_params.get('day') == 'tomorrow':
                next_day = timezone.now().date() + timedelta(days=1)
                queryset = MovieSession.objects.filter(
                    date_start__lte=next_day,
                    date_end__gte=next_day
                )

            sort_by = self.request.query_params.get('sort')

            if sort_by == 'time_start':
                queryset = MovieSession.objects.order_by('time_start')
            elif sort_by == '-time_start':
                queryset = MovieSession.objects.order_by('-time_start')
            elif sort_by == 'price':
                queryset = MovieSession.objects.order_by('price')
            elif sort_by == '-price':
                queryset = MovieSession.objects.order_by('-price')
        return queryset


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MovieSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseWriteSerializer
        return PurchaseReadSerializer

    def perform_create(self, serializer):
        try:
            session = serializer.validated_data.get('session')
            tickets = serializer.validated_data.get('tickets')

            session.bought_places += tickets

            total_amount = tickets * session.price

            customer = self.request.user

            customer.money -= total_amount

            with transaction.atomic():
                serializer.save(customer=customer, total_amount=total_amount)
                customer.save()
                session.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
