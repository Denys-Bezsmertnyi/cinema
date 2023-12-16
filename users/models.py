from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authentication import TokenAuthentication


class Customer(AbstractUser):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=5000)


class CustomerProfile(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="user_profile")
    money_spent = models.DecimalField(max_digits=10, decimal_places=2)

    # def purchase(self):
    #     return Purchase.objects.filter(user=self.user)

    def __str__(self):
        return self.user.username


class CustomTokenAuth(TokenAuthentication):
    keyword = 'Bearer'
