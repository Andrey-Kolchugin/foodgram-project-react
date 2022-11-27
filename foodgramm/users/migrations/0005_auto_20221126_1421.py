# Generated by Django 2.2.19 on 2022-11-26 11:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20221120_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='user',
            name='subscribe',
            field=models.ManyToManyField(related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписка'),
        ),
    ]
