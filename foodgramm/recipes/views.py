from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializer import TagSerializer, IngredientsSerializer, RecipesSerializer
from .models import Recipes, Tag, Ingredients, Favorite, ShoppingCart, IngredientInRecipe
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.response import Response
from django.db.models import Sum, F


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Получает queryset в соответствии с параметрами запроса.
        Returns:
            QuerySet: Список запрошенных объектов.
        """
        queryset = self.queryset

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        # Следующие фильтры только для авторизованного пользователя
        user = self.request.user
        if user.is_anonymous:
            return queryset

        is_in_shopping = self.request.query_params.get('is_in_shopping_cart')
        if is_in_shopping in ('1', 'true',):
            queryset = queryset.filter(id__in=ShoppingCart.objects.filter(user=user).values('recipes'))
        elif is_in_shopping in ('0', 'false',):
            queryset = queryset.exclude(id__in=ShoppingCart.objects.filter(user=user).values('recipes'))

        # is_favorited = self.request.query_params.get(conf.FAVORITE)
        # if is_favorited in conf.SYMBOL_TRUE_SEARCH:
        #     queryset = queryset.filter(favorite=user.id)
        # if is_favorited in conf.SYMBOL_FALSE_SEARCH:
        #     queryset = queryset.exclude(favorite=user.id)

        return queryset

    @action(detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        query = ShoppingCart.objects.filter(user=user)
        if not query.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = IngredientInRecipe.objects.filter(
            recipe__in=(query.values('recipes'))
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))
        filename = f'{user.username}_shopping_cart.txt'
        shopping_list = (
            f'Список покупок для:\n\n{user.username}\n\n'
            f'от {datetime.now()}\n\n'
        )
        for ing in ingredients:
            shopping_list += (
                f'{ing["ingredient"]}: {ing["amount"]} {ing["measure"]}\n'
            )

        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(methods=('POST', 'DELETE'), detail=True)
    def favorite(self, request, pk):
        recipes = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(
                    user=self.request.user,
                    recipes=recipes
            ).exists():
                content = {
                    "errors": "Рецепт уже в избранном!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite(user=self.request.user, recipes=recipes)
            favorite.save()
            return Response(status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Favorite.objects.filter(
                    user=self.request.user,
                    recipes=recipes
            ).exists():
                content = {
                    "errors": "Рецепт не в избранном!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.filter(user=self.request.user, recipes=recipes).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('POST', 'DELETE'), detail=True)
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipes = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    user=self.request.user, recipes=recipes
            ).exists():
                content = {
                    "errors": "Рецепт уже в корзине!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            shopping_cart = ShoppingCart(user=self.request.user, recipes=recipes)
            shopping_cart.save()
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                    user=self.request.user, recipes=recipes
            ).exists():
                content = {
                    "errors": "Рецепт уже не в корзине!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.filter(user=self.request.user, recipes=recipes).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
