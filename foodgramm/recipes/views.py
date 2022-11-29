from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializer import RecipesSerializer, TagSerializer, IngredientsSerializer
from .models import Recipes, Tag, Ingredients, Favorite
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.response import Response



class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    # permission_classes = (IsAuthenticated,)

    @action(methods=('POST', 'DELETE'), detail=True)
    def favorite(self, request, id):
        recipes = get_object_or_404(Recipes, pk=id)
        if request.method == 'POST':
            if Favorite.objects.filter(user=self.request.user, recipes=recipes).exists():
                content = {
                    "errors": "Рецепт уже в избранном!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite(user = self.request.user, recipes=recipes)
            favorite.save()
            return Response(status=status.HTTP_201_CREATED)

        # if request.method == 'DELETE':
        #     if not User.objects.filter(id=user.id, subscribe=following).exists():
        #         content = {
        #             "errors": "Подписки на этого пользователя не существует!"
        #         }
        #         return Response(content, status=status.HTTP_400_BAD_REQUEST)
        #     user.subscribe.remove(following)
        #     return Response(status=status.HTTP_204_NO_CONTENT)




class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()



