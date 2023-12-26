import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import views, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cinema_diploma import settings
from users.API.serializers import UserSerializer, UserRegisterSerializer, CustomerOrderSerializer
from users.models import Customer


class CustomAuthTokenLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        now = datetime.datetime.now()
        Token.objects.filter(user=user,
                             created__lt=now - datetime.timedelta(
                                 seconds=settings.TIME_SINCE_LAST_ACTION)).delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'token': token.key,
            'username': user.username
        })


class LogoutApiView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id__in=[self.request.user.pk])
        return queryset

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = []
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        elif self.request.method == 'GET' and self.request.query_params.get('profile', '') == 'yes':
            return CustomerOrderSerializer
        return UserSerializer

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=password)
        Token.objects.get_or_create(user=user)
