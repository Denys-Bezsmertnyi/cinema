from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authentication import TokenAuthentication


class Customer(AbstractUser):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=5000)


class CustomTokenAuth(TokenAuthentication):
    keyword = 'Bearer'
