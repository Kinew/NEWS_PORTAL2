from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from django.core.validators import MinValueValidator
from django.urls import reverse

from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy



class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAutor = pRat *3 + cRat
        self.save()

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text=_('category name'))
    subscribers = models.ManyToManyField(User, related_name= 'categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post',)

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


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreations = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


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


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )