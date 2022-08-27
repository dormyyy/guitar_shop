# Generated by Django 4.1 on 2022-08-20 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guitars', '0005_category_slug_guitars_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='guitars',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
