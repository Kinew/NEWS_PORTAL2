from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    NewsList, News, PostCreate, PostUpdate, PostDelete,
    subscribe, CategoryListView
)

urlpatterns = [
    path('news/', cache_page(60)(NewsList.as_view())),
    path('<int:pk>', cache_page(300)(News.as_view()), name = 'post_detail'),
    path('news/create/', cache_page(300)(PostCreate.as_view()), name='news_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('category/<int:pk>', CategoryListView.as_view(), name= 'category.list'),
    path('category/<int:pk>/subscribe', subscribe, name= 'subscribe')
]