from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from .serializers import UserSerializer
from rest_framework.mixins import ListModelMixin


User = get_user_model()


class UserViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
