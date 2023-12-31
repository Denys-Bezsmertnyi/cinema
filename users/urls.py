from django.urls import path, include

from users.views import UserLoginView, UserRegisterView, UserLogoutView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('api/', include('users.API.urls')),
]
