from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class Ingredients(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField()
    measurement_unit = models.CharField()

    class Meta:
        verbose_name = 'Интгридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True)
    color = models.TextField()
    slug = models.SlugField(unique=True)


class Recipes(models.Model):
    """
    Класс работы с рецептами
    """
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=False,
        related_name='author',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        on_delete=models.CASCADE,
        blank=False,
        related_name='recipe',
        verbose_name='Рецепт'
    )
    tags = models.ManyToManyField(
        Tag,
        on_delete=models.SET_NULL,
        blank=False,
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


