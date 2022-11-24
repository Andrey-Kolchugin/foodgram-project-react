from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializer import RecipesSerializer, TagSerializer, FavoriteSerializer
from .models import Recipes, Tag, Favorite
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        recipes = get_object_or_404(
            Recipes,
            id=self.kwargs.get('recipes_id'),
        )
        serializer.save(author=self.request.user, recipes=recipes)
