from rest_framework import status
from rest_framework.response import Response

from cinema.models import MovieSession, CinemaHall


class CheckPurchasedTicketsMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if isinstance(instance, MovieSession):
            if instance.bought_places > 0:
                return Response({"detail": "Cannot delete session with purchased tickets."},
                                status=status.HTTP_400_BAD_REQUEST)

        elif isinstance(instance, CinemaHall):
            sessions_with_purchased_tickets = MovieSession.objects.filter(hall=instance, bought_places__gt=0)
            if sessions_with_purchased_tickets.exists():
                return Response({"detail": "Cannot delete hall with sessions containing purchased tickets."},
                                status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)
