from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from django.core.cache import cache

from django.core.validators import MinValueValidator
from django.urls import reverse

from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class News(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0')])
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def get_absolute_url(self):
        return f'/post/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class Author(models.Model):
    full_name = models.CharField(max_length=64)
    name = models.CharField(null=True, max_length=64)

    def some_method(self):
        self.name = self.full_name.split()[0]

    self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post', )

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreations = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    added_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.title.title()}: {self.text[:10]}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


class Response(models.Model):
    pass
