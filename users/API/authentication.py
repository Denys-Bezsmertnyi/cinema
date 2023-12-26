import datetime

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from cinema_diploma import settings


class TokenExpiredAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        expiration_time = token.created + timezone.timedelta(seconds=settings.TIME_SINCE_LAST_ACTION)

        if timezone.now() > expiration_time:
            token.delete()
            raise AuthenticationFailed(f'Token was created more than {settings.TIME_SINCE_LAST_ACTION} seconds ago.')

        return token.user, token
