from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Ingredients, Recipes, Tag, Favorite

User = get_user_model()


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    empty_value_display = '-пусто-'


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'image', 'name', 'cooking_time')
    empty_value_display = '-пусто-',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipes')
    empty_value_display = '-пусто-'
