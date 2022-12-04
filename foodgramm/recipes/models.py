from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class Ingredients(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единица измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'Интгридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.ImageField(
        verbose_name='Картинка',
        null=True,
        blank=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    """
    Класс работы с рецептами
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='author',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        blank=False,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='tags',
        verbose_name='Тег'
    )
    image = models.TextField(
        blank=False,
        verbose_name='Picture'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название блюда',
        unique=True,
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, 'Число должно быть от 1 до 60!'),
                    MaxValueValidator(60, 'Число должно быть от 1 до 60!')],
        blank=False
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='user',
        verbose_name='Юзер',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        blank=False,
        related_name='recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        unique_together = ['user', 'recipes']
        verbose_name = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='shoppin_cart_user',
        verbose_name='Юзер',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        blank=True,
        related_name='shoppin_cart_recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        unique_together = ['user', 'recipes']
        verbose_name = 'Корзина'


# class AmountIngredient(models.Model):
#     """
#     Количество ингридиентов в блюде.
#     """
#     recipe = models.ForeignKey(
#         Recipes,
#         verbose_name='Используется в этих рецептах',
#         related_name='ingredient',
#         on_delete=models.CASCADE,
#     )
#     ingredients = models.ForeignKey(
#         Ingredients,
#         verbose_name='Связанные ингредиенты',
#         related_name='recipe',
#         on_delete=models.CASCADE,
#     )
#     amount = models.PositiveSmallIntegerField(
#         verbose_name='Количество',
#         default=1,
#         validators=(
#             MinValueValidator(
#                 1, 'Должно быть указано количество!'
#             ),
#             MaxValueValidator(
#                 10000, 'Зачем вам так много?'
#             ),
#         ),
#     )
#
#     class Meta:
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'Ингредиенты'
#         ordering = 'recipe',
#         unique_together = ['recipe', 'ingredients']
#
#     def __str__(self):
#         return f'{self.amount} {self.ingredients}'
