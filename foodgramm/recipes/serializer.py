from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tag, Ingredients, Recipes, Favorite


User = get_user_model()


class RecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецептов.
    """

    class Meta:
        model = Recipes
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов.
    """

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__']


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для избранного.
    """

    class Meta:
        model = Favorite
        fields = '__all__'
        # read_only_fields = ['__all__']