import time

import pytz
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.base import ContextMixin

from .models import *
from .filters import PostFilter
from .forms import PostForm, TimezoneForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .tasks import notify_subscribers

from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework import permissions
from news.serializers import *



class BaseContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = self.request.GET.get('timezone')

        if user_timezone:
            timezone.activate(user_timezone)

        context['current_time'] = timezone.localtime(timezone.now())
        context['timezone_form'] = TimezoneForm()
        context['server_time'] = self.request.server_time

        return context


class PostsList(BaseContextMixin, ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'

    paginate_by = 2


class PostDetail(BaseContextMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk)
        return render(request, 'news.html', {'post': post})


class SearchPost(BaseContextMixin, ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = '-created_at'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CreatePost(BaseContextMixin, LoginRequiredMixin, PermissionRequiredMixin,  CreateView):  # добавлен вызов задачи из tasks
    model = Post
    template_name = 'add.html'
    context_object_name = 'news'
    ordering = '-created_at'
    paginate_by = 5
    form_class = PostForm
    permission_required = 'news.add_post'
    success_url = '/news'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_post = form.save()
            notify_subscribers.delay(new_post.pk)   # вызов задачи на отправку письма подписчикам, при создании поста
            return redirect('post_detail', pk=new_post.pk)

        return super().get(request, *args, **kwargs)


class PostUpdate(BaseContextMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = 'news.change_post'

    def get_object(self, **kwargs):  # для кэширования D11
        id_post = self.kwargs.get('pk')
        obj = cache.get(f'post-{id_post}', None)
        if not obj:
            obj = Post.objects.get(pk=id_post)
            cache.set(f'post-{id_post}', obj)
        return obj


class PostDelete(BaseContextMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news'
    permission_required = 'news.delete_post'


class IndexView(BaseContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news'


class UpgradeView(BaseContextMixin, CreateView):
    @login_required
    def upgrade_me(self, request, *args, **kwargs):
        user = request.user
        authors_group = Group.objects.get(name='authors')
        if not request.user.groups.filter(name='authors').exists():
            authors_group.user_set.add(user)
        return redirect('/news')


@login_required
def subscribe_category(request, pk):
    category = Category.objects.get(pk=pk)
    request.user.subscribed_categories.add(category)
    return redirect('/news/categories')


@login_required
def unsubscribe_category(request, pk):
    category = Category.objects.get(pk=pk)
    request.user.subscribed_categories.remove(category)
    return render(request, 'unsubscription_category.html')


class Categories(BaseContextMixin, LoginRequiredMixin, ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'category_list'


class Subscription(BaseContextMixin, LoginRequiredMixin, ListView):
    template_name = 'subscription.html'
    model = Category
    context_object_name = 'category_list'


class PostsInCategoryList(BaseContextMixin, ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news_in_category.html'
    context_object_name = 'news'

    paginate_by = 5

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Post.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer


class CategoryViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer


class PostViewest(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


class PostCategoryViewest(viewsets.ModelViewSet):
   queryset = PostCategory.objects.all()
   serializer_class = PostCategorySerializer


class CommentViewest(viewsets.ModelViewSet):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer


class NewsListView(generics.ListAPIView):
    queryset = Post.objects.filter(post_type='news')
    serializer_class = PostSerializer


class ArticleListView(generics.ListAPIView):
    queryset = Post.objects.filter(post_type='article')
    serializer_class = PostSerializer

