from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cinema.API.serializers import PurchaseReadSerializer
from cinema.models import Purchase
from users.models import Customer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = Customer
        fields = ['id', 'username', 'password', 'password2', 'token']

    def validate(self, attrs):
        if Customer.objects.filter(username=attrs['username']).count():
            raise ValidationError("User with this username already exists")

        if attrs['password'] != attrs['password2']:
            raise ValidationError("Passwords are different")
        attrs.pop('password2')
        return attrs


class CustomerOrderSerializer(serializers.ModelSerializer):
    total_spent = serializers.SerializerMethodField()
    purchases = PurchaseReadSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'total_spent', 'purchases']

    def get_total_spent(self, obj):
        user = self.context['request'].user
        return Purchase.objects.filter(customer=user).aggregate(Sum('total_amount'))['total_amount__sum']
