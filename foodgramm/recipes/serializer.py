from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Tag, Ingredients, Recipes, Favorite
from drf_extra_fields.fields import Base64ImageField
from users.serializers import CustomUserSerializer
from django.db.models import F


User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингридиентов.
    """

    class Meta:
        model = Ingredients
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов.
    """

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__']


class RecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рецептов.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    # is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()
    ingredients = IngredientsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = '__all__'

    def get_ingredients(self, obj):
        """
        Получает список ингридиентов для рецепта.
        """
        ingredients = obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        """
        Проверка - находится ли рецепт в избранном.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipes=obj).exists()
    #
    # def get_is_in_shopping_cart(self, obj):
    #     """Проверка - находится ли рецепт в списке  покупок.
    #     Args:
    #         obj (Recipe): Переданный для проверки рецепт.
    #     Returns:
    #         bool: True - если рецепт в `списке покупок`
    #         у запращивающего пользователя, иначе - False.
    #     """
    #     user = self.context.get('request').user
    #     if user.is_anonymous:
    #         return False
    #     return user.carts.filter(id=obj.id).exists()

    # def create(self, validated_data):
    #     """Создаёт рецепт.
    #     Args:
    #         validated_data (dict): Данные для создания рецепта.
    #     Returns:
    #         Recipe: Созданый рецепт.
    #     """
    #     image = validated_data.pop('image')
    #     tags = validated_data.pop('tags')
    #     ingredients = validated_data.pop('ingredients')
    #     recipe = Recipe.objects.create(image=image, **validated_data)
    #     recipe.tags.set(tags)
    #     recipe_amount_ingredients_set(recipe, ingredients)
    #     return recipe
    #
    # def update(self, recipe, validated_data):
    #     """Обновляет рецепт.
    #     Args:
    #         recipe (Recipe): Рецепт для изменения.
    #         validated_data (dict): Изменённые данные.
    #     Returns:
    #         Recipe: Обновлённый рецепт.
    #     """
    #     tags = validated_data.get('tags')
    #     ingredients = validated_data.get('ingredients')
    #
    #     recipe.image = validated_data.get(
    #         'image', recipe.image)
    #     recipe.name = validated_data.get(
    #         'name', recipe.name)
    #     recipe.text = validated_data.get(
    #         'text', recipe.text)
    #     recipe.cooking_time = validated_data.get(
    #         'cooking_time', recipe.cooking_time)
    #
    #     if tags:
    #         recipe.tags.clear()
    #         recipe.tags.set(tags)
    #
    #     if ingredients:
    #         recipe.ingredients.clear()
    #         recipe_amount_ingredients_set(recipe, ingredients)
    #
    #     recipe.save()
    #     return recipe
