from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    """Модель пользователя с кастомными полями"""
    email = models.EmailField(
        max_length=254,
        help_text='Адрес электронной почты',
        verbose_name='Адрес электронной почты',
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        blank=False,
    )
    subscribe = models.ManyToManyField(
        verbose_name='Подписка',
        related_name='subscribers',
        to='self',
        symmetrical=False,
        blank=True
    )
    # recipes = models.ForeignKey(
    #     Recipes,
    #     verbose_name='рецепты',
    #     related_name='recipes',
    #     on_delete = models.SET_NULL,
    #     blank=True
    # )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# class Follow(models.Model):
#     """Модель подписки на авторов"""
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Подписчик'
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Автор'
#     )
#
#     class Meta:
#         verbose_name = 'Фолловер'
#         verbose_name_plural = 'Списки подписчиков'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["author", "user"], name="unique_following"
#             )
#         ]
