from django.contrib import admin
from .models import MyModel, Category
from modeltranslation.admin import \
    TranslationAdmin  # импортируем модель админки (вспоминаем модуль про переопределение стандартных админ-инструментов)


# Register your models here.

# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = MyModel


admin.site.register(MyModel)
admin.site.register(Category)

# Register your models here.
