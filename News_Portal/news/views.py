from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)

from django.utils.translation import gettext as _


from .models import Post, Category
from .forms import PostForm
from .filters import PostFilter


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreations'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2
# Create your views here.

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


 # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class News(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_obgect_name = 'post'


# Добавляем новое представление для создания товаров.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal.add_post',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'
    context_object_name = 'create'


    def form_valid(self, form):
        post = form.save(commit = False)
        if self.request.path == '/articles/create/':
            post.post_news = 'AR'
        return super().form_valid(form)



# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_portal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'name/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id= self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
@csrf_protect
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    mesage = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news/subscriptions.html', {'category':category, 'mesage': mesage})


class Index(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'index.html', context))

