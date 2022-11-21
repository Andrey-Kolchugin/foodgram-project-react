from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserSerializer, UserCreateSerializer

from .models import Follow


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для простмотра юзеров."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для простмотра юзеров."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }