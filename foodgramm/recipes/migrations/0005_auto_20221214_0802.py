# Generated by Django 2.2.19 on 2022-12-14 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221211_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, default='FF', max_length=7, null=True, verbose_name='Цветовой HEX-код'),
        ),
    ]
