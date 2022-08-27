from django.contrib import admin
from .models import Guitars, Category

# Register your models here.


class GuitarsConfig(admin.ModelAdmin):
    list_display = ('name', 'is_published',)
    list_display_links = ('name',)
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryConfig(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Guitars, GuitarsConfig)
admin.site.register(Category, CategoryConfig)
