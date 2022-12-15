from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredients, Recipes, ShoppingCart, Tag
from recipes.serializer import (IngredientsSerializer, RecipesSerializer,
                                RecipeWriteSerializer, TagSerializer)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.serializers import (CustomUserSerializer, ShortRecipeSerializer,
                               UserSubscribeSerializer)

from . import conf
from .filters import IngredientFilter
from .paginators import PageLimitPagination
from .permissions import AdminOrReadOnly, AuthorStaffOrReadOnly
from .ervice import add_or_delete_obj, get_shopping_cart_txt

User = get_user_model()


class UserListViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = PageLimitPagination

    def get_queryset(self):
        return User.objects.all()

    @action(methods=('GET',), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        result_page = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            result_page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=('POST', 'DELETE'), detail=True)
    def subscribe(self, request, id):

        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        following = get_object_or_404(User, pk=id)
        if request.method == 'POST':

            if User.objects.filter(id=user.id, subscribe=following).exists():
                content = {
                    "errors": "Подписка на этого пользователя уже существует!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            if user.id == following.id:
                content = {
                    "errors": "Нельзя подписываться на самого себя!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            user.subscribe.add(following)
            self.request.user = following
            serializer = UserSubscribeSerializer(
                context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not User.objects.filter(
                    id=user.id, subscribe=following).exists():
                content = {
                    "errors": "Подписки на этого пользователя не существует!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            user.subscribe.remove(following)
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (AuthorStaffOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_serializer_class(self):
        """
        В зависимости от метода
        возвращает нужный сериалайзер
        """
        if self.request.method in SAFE_METHODS:
            return RecipesSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        """
        Получает queryset в соответствии с параметрами запроса.
        """
        queryset = self.queryset

        tags = self.request.query_params.getlist(conf.TAGS)

        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get(conf.AUTHOR)
        if author:
            queryset = queryset.filter(author=author)
        user = self.request.user
        if user.is_anonymous:
            return queryset

        is_in_shopping = self.request.query_params.get(conf.SHOP_CART)
        if is_in_shopping in conf.SYMBOL_TRUE:
            queryset = queryset.filter(
                id__in=ShoppingCart.objects.filter(user=user).values('recipes')
            )
        elif is_in_shopping in conf.SYMBOL_FALSE:
            queryset = queryset.exclude(
                id__in=ShoppingCart.objects.filter(user=user).values('recipes')
            )

        is_favorited = self.request.query_params.get(conf.FAVORITE)
        if is_favorited in conf.SYMBOL_TRUE:
            queryset = queryset.filter(
                id__in=Favorite.objects.filter(user=user).values('recipes')
            )
        if is_favorited in conf.SYMBOL_FALSE:
            queryset = queryset.exclude(
                id__in=Favorite.objects.filter(user=user).values('recipes')
            )

        return queryset

    @action(detail=False)
    def download_shopping_cart(self, request):
        """
        Скачивает ингр-ты и кол-во из корзины.
        Функция создания txt импортируется
        из модуля service
        """
        user = self.request.user
        if user.is_anonymous:
            Response(status=status.HTTP_401_UNAUTHORIZED)
        query = ShoppingCart.objects.filter(user=user)
        if not query.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return get_shopping_cart_txt(query, user)

    @action(methods=('POST', 'DELETE'), detail=True)
    def favorite(self, request, pk):
        """
        Метод добавляет или удаляет рецепт в избранное
        """
        recipes = get_object_or_404(Recipes, pk=pk)
        user = self.request.user
        if request.method == 'POST':
            return Response(add_or_delete_obj(
                user=user,
                recipes=recipes,
                action=conf.METHOD_ADD,
                model=Favorite),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            add_or_delete_obj(
                user=user,
                recipes=recipes,
                action=conf.METHOD_DEL,
                model=Favorite),
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('POST', 'DELETE'), detail=True)
    def shopping_cart(self, request, pk):
        """
        Метод добавляет или удаляет рецепт в корзину
        """
        user = self.request.user
        recipes = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            return Response(add_or_delete_obj(
                user=user,
                recipes=recipes,
                action=conf.METHOD_ADD,
                model=ShoppingCart),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            add_or_delete_obj(
                user=user,
                recipes=recipes,
                action=conf.METHOD_DEL,
                model=ShoppingCart),
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AdminOrReadOnly,)
