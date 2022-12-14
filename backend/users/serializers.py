from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import Recipes

User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe
    с укороченными полями.
    """
    class Meta:
        model = Recipes
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для просмотра юзеров.
    """
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
    """
    Сериализатор вывода авторов, на которых подписан текущий пользователь.
    """

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

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
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        """
        Метод всегда возвращает True
        для экономии подходов в базу
        """
        return True

    def get_recipes_count(self, obj):
        """
        Метод возвращает количество рецептов
        """
        return Recipes.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        """
        Метод определяет и возвращает короткий вариант рецептов
        """
        recipe = Recipes.objects.filter(author=obj)
        serializer = ShortRecipeSerializer(recipe, many=True, read_only=True)
        return serializer.data


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для простмотра юзеров.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
