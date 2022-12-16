from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from users.serializers import CustomUserSerializer

from .models import (Favorite, IngredientInRecipe, Ingredients, Recipes,
                     ShoppingCart, Tag)

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
        read_only_fields = '__all__',


class RecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения рецептов.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

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

    def get_is_in_shopping_cart(self, obj):
        """
        Проверка - находится ли рецепт в списке  покупок.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipes=obj).exists()

    def validate(self, data):
        """
        Проверка вводных данных при создании/редактировании рецепта.
        """
        name = str(self.initial_data.get('name')).strip()
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        values_as_list = (tags, ingredients)

        for value in values_as_list:
            if not isinstance(value, list):
                raise ValidationError(
                    f'"{value}" должен быть в формате "[]"'
                )
        data['name'] = name.capitalize()
        data['tags'] = tags
        data['author'] = self.context.get('request').user
        return data


class IngredientsWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингридиентов.
    """

    class Meta:
        model = IngredientInRecipe
        fields = ('ingredient', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингр-ов и их кол-ва в каждом рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all()
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления рецептов
    """
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.ListField(
        child=serializers.SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all(),
        ),
    )
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    @staticmethod
    def create_ingredients(ingredients, recipe):
        objs = [
            IngredientInRecipe(
                recipe=recipe,
                ingredients=ingredient['id'],
                amount=ingredient['amount'],
            ) for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(objs)

    @transaction.atomic
    def create(self, validated_data):
        """
        Метод создание рецепта.
        """
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, recipe):
        """
        Сериализатор возвращает результат работы методов.
        """
        return RecipesSerializer(recipe, context=self.context).data

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Метод обновления рецетов
        """
        instance.ingredients.clear()
        instance.tags.clear()
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.set(tags)
        self.create_ingredients(ingredients, recipe=instance)
        return super().update(instance, validated_data)
