import django.contrib.auth.models
from django.db import models
from django.conf import settings


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    cat_type = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name_plural = 'Categories'


class Guitars(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.FloatField(null=False, verbose_name='Ціна')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    published_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_published = models.BooleanField(default=True, verbose_name='Публікація')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='Автор')
    category = models.ManyToManyField(Category, verbose_name='Категорія')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Guitars'
        ordering = ['-published_time']
