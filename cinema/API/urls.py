from rest_framework import routers
from django.urls import path, include

from cinema.API.resources import HallViewSet, SessionViewSet, MovieViewSet, PurchaseViewSet

router = routers.SimpleRouter()
router.register(r'hall', HallViewSet)
router.register(r'session', SessionViewSet)
router.register(r'movie', MovieViewSet)
router.register(r'purchase', PurchaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
