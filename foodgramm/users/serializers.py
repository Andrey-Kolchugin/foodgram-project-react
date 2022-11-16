from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя общего назначения."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SignUpSerializer(serializers.ModelSerializer):
    """Регистрация пользователя."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
    # валидатор не используется
    # def validate_username(self, value):
    #     if value == 'me':
    #         raise serializers.ValidationError(
    #             'Имя пользователя "me" использовать нельзя!')
    #     return value
