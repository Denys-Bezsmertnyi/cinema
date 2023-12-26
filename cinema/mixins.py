from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.shortcuts import redirect
from cinema.models import MovieSession, CinemaHall


class AdminRequiredMixin(UserPassesTestMixin, AccessMixin):
    login_url = '/login'

    def test_func(self):
        return self.request.user.is_superuser


class HallAndSessionMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if isinstance(self.object, MovieSession) and self.object.bought_places > 0:
            messages.error(self.request, "Session with bought tickets.")
            return redirect('cinema:session_list')

        if isinstance(self.object, CinemaHall) and hasattr(self.object, 'sessions') and any(
                session.bought_places > 0 for session in self.object.sessions.all()):
            messages.error(self.request, "Hall has sessions with bought tickets.")
            return redirect('cinema:hall_list')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if isinstance(self.object, MovieSession) and self.object.bought_places > 0:
            messages.error(self.request, "Session has already had bought tickets.")
            return redirect('cinema:session_list')

        if isinstance(self.object, CinemaHall) and hasattr(self.object, 'sessions') and any(
                session.bought_places > 0 for session in self.object.sessions.all()):
            messages.error(self.request, "Hall has sessions with bought tickets.")
            return redirect('cinema:hall_list')

        return super().post(request, *args, **kwargs)
