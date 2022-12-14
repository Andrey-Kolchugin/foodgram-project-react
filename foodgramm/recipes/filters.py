from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from .models import Ingredients
from rest_framework.filters import SearchFilter

User = get_user_model()


class IngredientFilter(SearchFilter):
    """Products search filter model."""
    search_param = 'name'

    class Meta:
        model = Ingredients
        fields = ('name',)


# class RecipeFilter(FilterSet):
#     """Recipe search filter model."""
#     tags = filters.ModelMultipleChoiceFilter(
#         field_name='tags__slug',
#         to_field_name='slug',
#         queryset=Tag.objects.all(),
#     )
#     author = filters.ModelChoiceFilter(queryset=User.objects.all())
#     is_favorited = filters.BooleanFilter(method='if_is_favorited')
#     is_in_shopping_cart = filters.BooleanFilter(
#         method='if_is_in_shopping_cart'
#     )

    # class Meta:
    #     model = Recipe
    #     fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)
    #
    # def if_is_favorited(self, queryset, name, value):
    #     """'is_favorited' parameter filter processing method."""
    #     if value and self.request.user.is_authenticated:
    #         return queryset.filter(favorites__user=self.request.user)
    #     return queryset
    #
    # def if_is_in_shopping_cart(self, queryset, name, value):
    #     """'if_is_in_shopping_cart' parameter filter processing method."""
    #     if value and self.request.user.is_authenticated:
    #         return queryset.filter(shopping_list__user=self.request.user)
    #     return
