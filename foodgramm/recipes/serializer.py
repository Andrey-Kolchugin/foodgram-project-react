from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tag, Ingredients, Recipes, Favorite


User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка избранного.
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    recipes = serializers.IntegerField


    class Meta:
        model = Favorite
        fields = '__all__'





class IngredientsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингридиентов.
    """

    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецептов.
    """
    ingredients = IngredientsSerializer(many=True, read_only=True)

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
