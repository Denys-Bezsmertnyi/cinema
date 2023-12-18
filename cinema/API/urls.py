from rest_framework import routers
from django.urls import path, include

from cinema.API.resources import HallViewSet, SessionViewSet, MovieViewSet

router = routers.SimpleRouter()
router.register(r'hall', HallViewSet)
router.register(r'session', SessionViewSet)
router.register(r'movie', MovieViewSet)


urlpatterns = [
    path('', include(router.urls)),
]