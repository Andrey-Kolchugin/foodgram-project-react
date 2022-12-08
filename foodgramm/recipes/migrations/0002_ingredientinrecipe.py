# Generated by Django 2.2.19 on 2022-12-08 15:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Укажите кол-во от 1 до 9999'), django.core.validators.MaxValueValidator(9999, 'Укажите кол-во от 1 до 9999')], verbose_name='Количество')),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.Ingredients', verbose_name='Ингредиенты в этом рецепте')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.Recipes', verbose_name='Рецепт для этих ингредиентов')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в репепте',
                'ordering': ('pk',),
                'unique_together': {('recipe', 'ingredients')},
            },
        ),
    ]
