from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'

    paginate_by = 2


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk)
        return render(request, 'news.html', {'post': post})


class SearchPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = '-created_at'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin,  CreateView):
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
            form.save()

        return super().get(request, *args, **kwargs)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = 'news.change_post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news'
    permission_required = 'news.delete_post'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


@login_required
def subscribe_category(request, pk):
    category = Category.objects.get(pk=pk)
    request.user.subscribed_categories.add(category)
    return render(request, 'subscription_category.html')


@login_required
def unsubscribe_category(request, pk):
    category = Category.objects.get(pk=pk)
    request.user.subscribed_categories.remove(category)
    return render(request, 'unsubscription_category.html')


class Categories(LoginRequiredMixin, ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'category_list'


class Subscription(LoginRequiredMixin, ListView):
    template_name = 'subscription.html'
    model = Category
    context_object_name = 'category_list'


class PostsInCategoryList(ListView):
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

