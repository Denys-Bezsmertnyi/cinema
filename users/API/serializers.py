from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

# class CustomerProfileSerializer(serializers.ModelSerializer):