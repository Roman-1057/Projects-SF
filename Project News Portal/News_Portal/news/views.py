from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'

    paginate_by = 2  # вывод в 2 страницы


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
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin,  CreateView):
    model = Post
    template_name = 'add.html'
    context_object_name = 'news'
    ordering = '-created_at'
    paginate_by = 1
    form_class = PostForm
    permission_required = 'news.add_post'

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


@login_required
def notify_subscribers(request, category, post):
    user = request.user
    subject = post.title
    message = f"Здравствуй, {user.username}. Новая статья в твоем любимом разделе!"
    html_message = render_to_string('email_template.html', {'post': post})

    subscribers = category.subscribers.all()
    recipient_list = [user.email for user in subscribers]

    send_mail(subject, message, None, recipient_list, html_message=html_message)
