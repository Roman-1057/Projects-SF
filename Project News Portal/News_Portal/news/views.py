# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    def post_sort(request):
        posts = Post.objects.order_by('-created_at')  # Сортировка по убыванию даты публикации

        context = {
            'news': posts,
        }

        return render(request, 'news.html', context)


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
