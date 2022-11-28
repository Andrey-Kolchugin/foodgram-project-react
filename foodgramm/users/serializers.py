from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserSerializer, UserCreateSerializer

from recipes.models import Recipes
from recipes.serializer import RecipesSerializer


User = get_user_model()


class ShortRecipeSerializer(ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов.
    """
    class Meta:
        model = Recipes
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class CustomUserSerializer(UserSerializer):
    """Сериализатор для просмотра юзеров."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()




class UserSubscribeSerializer(CustomUserSerializer):
    """Сериализатор вывода авторов на которых подписан текущий пользователь.
    """
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    # recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            # 'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        return True

    # def get_recipes_count(self, obj):
    #     return obj.recipes.count()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для простмотра юзеров."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
