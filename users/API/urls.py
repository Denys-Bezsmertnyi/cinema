from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


from rest_framework import routers

from users.API.resources import UserViewSet, LogoutApiView

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('logout/', LogoutApiView.as_view()),
]