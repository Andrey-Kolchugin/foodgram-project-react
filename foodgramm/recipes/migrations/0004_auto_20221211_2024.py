# Generated by Django 2.2.19 on 2022-12-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221211_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recipes.Tag', verbose_name='Тег'),
        ),
    ]
