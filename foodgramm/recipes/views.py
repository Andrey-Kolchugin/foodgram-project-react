from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializer import TagSerializer, IngredientsSerializer, RecipesSerializer
from .models import Recipes, Tag, Ingredients, Favorite, ShoppingCart
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

    # @action(detail=False)
    # def download_shopping_cart(self, request):
    #     user = self.request.user
    #     queryset1 = ShoppingCart.objects.filter(user=user).values_list('recipes')
    #     queryset2 = Recipes.objects.filter(id__in=queryset1)
    #     test = Recipes.objects.get(id=2)
    #     test2 = test.ingredients.all().values_list('name')
    #     # queryset3 = queryset2.to_ingredients.all()
    #     print(test2)

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
