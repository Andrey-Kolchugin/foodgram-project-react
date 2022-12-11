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
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=6,
        blank=True,
        null=True,
        default='FF'
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
        to=Ingredients,
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
                    MaxValueValidator(60, 'Число должно быть от 1 до 60!')],
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
        unique_together = ['author', 'name']


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
        related_name='to_recipes',
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


class IngredientInRecipe(models.Model):
    """
    Ингредиенты в каждом рецепте.
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
        unique_together = ['recipe', 'ingredients']

    def __str__(self):
        return f'{self.amount} {self.ingredients}'
