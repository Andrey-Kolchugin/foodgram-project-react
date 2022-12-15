from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from colorfield.fields import ColorField

User = get_user_model()


class Ingredients(models.Model):
    """
    Модель ингредиентов
    """
    id = models.AutoField(
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=30,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Интгридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    """
    Модель тегов
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        blank=True,
        null=True,
        default='#FF0000'
    )
    slug = models.CharField(
        unique=True,
        verbose_name='Слаг тега',
        max_length=50
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    """
    Модель рецептов
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
        verbose_name='Ингредиенты',
        through='recipes.IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Тег'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название блюда',
        unique=True,
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, 'Число должно быть от 1 до 60!'),
                    MaxValueValidator(999, 'Число должно быть от 1 до 999!')],
        blank=False
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        max_length=500,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'], name="unique_recipe"
            )
        ]


class Favorite(models.Model):
    """
    Модель категории избранных рецептов
    """
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
        related_name='to_recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'], name="unique_following"
            )
        ]


class ShoppingCart(models.Model):
    """
    Модель корзины покупок
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='shopping_cart',
        verbose_name='Юзер',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        blank=True,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'], name="unique_shopping_cart"
            )
        ]


class IngredientInRecipe(models.Model):
    """
    Модель ингредиентов и их кол-ва в каждом рецепте.
    """
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт для этих ингредиентов',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredients,
        verbose_name='Ингредиенты в этом рецепте',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
        validators=(
            MinValueValidator(
                1, 'Укажите кол-во от 1 до 9999'
            ),
            MaxValueValidator(
                9999, 'Укажите кол-во от 1 до 9999'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в репепте'
        ordering = 'pk',
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'], name="unique_ing_in_rec"
            )
        ]
