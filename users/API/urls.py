from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


from rest_framework import routers

from users.API.resources import UserViewSet, LogoutApiView, CustomAuthTokenLogin

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthTokenLogin.as_view()),
    path('logout/', LogoutApiView.as_view()),
]