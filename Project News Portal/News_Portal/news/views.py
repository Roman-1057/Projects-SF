# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    paginate_by = 2  # поставим постраничный вывод в один элемент

    # def post_sort(request):
    #     posts = Post.objects.order_by('-created_at')  # Сортировка по убыванию даты публикации
    #
    #     context = {
    #         'news': posts,
    #     }
    #
    #     return render(request, 'news.html', context)


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk)
        # Ваш код для отображения деталей поста
        return render(request, 'news.html', {'post': post})


class SearchPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = '-created_at'
    paginate_by = 1  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод
        # get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # вписываем наш фильтр в контекст
        return context


class CreatePost(ListView):
    model = Post
    template_name = 'create_post.html'
    context_object_name = 'news'
    ordering = '-created_at'
    paginate_by = 1  # поставим постраничный вывод в один элемент
    form_class = PostForm

    # def post(self, request, *args, **kwargs):
    #     # берём значения для нового товара из POST-запроса, отправленного на сервер
    #     title = request.POST['title']
    #     text = request.POST['text']
    #     category_id = request.POST.get('category')
    #     author = request.POST['author']
    #     post_type = request.POST['post_type']
    #
    #     post = Post(title=title, text=text, category_id=category_id, author=author, post_type=post_type)  # создаём новый товар и сохраняем
    #     post.save()
    #     return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
