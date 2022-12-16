from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Favorite, Ingredients, Recipes, ShoppingCart
from rest_framework.filters import SearchFilter

User = get_user_model()


class IngredientFilter(SearchFilter):
    """
    Фильтр поиска ингредиента.
    """
    search_param = 'name'

    class Meta:
        model = Ingredients
        fields = ('name',)


class RecipeFilter(FilterSet):
    """Recipe search filter model."""
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='if_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='if_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)

    def if_is_favorited(self, queryset, name, value):
        """'is_favorited' parameter filter processing method."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(id__in=Favorite.objects.filter(user=self.request.user).values('recipes'))
        return queryset

    def if_is_in_shopping_cart(self, queryset, name, value):
        """'if_is_in_shopping_cart' parameter filter processing method."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(id__in=ShoppingCart.objects.filter(user=self.request.user).values('recipes'))
        return
