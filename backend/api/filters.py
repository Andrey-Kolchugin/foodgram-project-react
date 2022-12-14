from django.contrib.auth import get_user_model
from recipes.models import Ingredients
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
