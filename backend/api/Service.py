from datetime import datetime

from django.db.models import F, Sum
from django.http import HttpResponse
from recipes.models import IngredientInRecipe
from rest_framework import status
from rest_framework.response import Response
from users.serializers import ShortRecipeSerializer

from . import conf


def get_shopping_cart_txt(query, user):
    """
    Функция получает обьект корзины
    и возвращает txt файл с ингр-ми и их кол-вом
    """
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


def add_or_delete_obj(action, model, user, recipes):
    """
    Функция добавляет или удаляет объект в БД
    """
    if action == conf.METHOD_ADD:
        if model.objects.filter(
                user=user, recipes=recipes
        ).exists():
            content = {
                "errors": "Объект уже существует!"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        model(user=user, recipes=recipes).save()
        return ShortRecipeSerializer(recipes, read_only=True).data

    if action == conf.METHOD_DEL:
        if not model.objects.filter(
                user=user, recipes=recipes
        ).exists():
            content = {
                "errors": "Обьекта уже не существует!"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        model.objects.filter(
            user=user, recipes=recipes).delete()
        return Response()
