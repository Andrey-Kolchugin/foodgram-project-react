from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .serializer import RecipesSerializer, TagSerializer, IngredientsSerializer, FavoriteSerializer
from .models import Recipes, Tag, Favorite, Ingredients
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins



class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    # permission_classes = (IsAuthenticated,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteSerializer

    # def get_queryset(self):
    #     return get_object_or_404(
    #         Recipes,
    #         id=self.kwargs.get('recipes_id'))

    def perform_create(self, serializer):
        # user = self.requests.user
        recipes = get_object_or_404(
            Recipes,
            id=serializer.data.get('id')
        )
        print(serializer.data)
        serializer.save()
