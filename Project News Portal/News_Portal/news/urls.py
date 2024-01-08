from django.urls import path, include
from django.views.generic import TemplateView
from django_apscheduler import admin

from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', PostsList.as_view()),
    path('index', IndexView.as_view()),
    path('search', SearchPost.as_view(), name='search_post'),
    path('add', CreatePost.as_view(), name='create_post'),
    path('<int:pk>', PostDetail.as_view()),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>', PostDetail.post_detail, name='post_detail'),
    path('login',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('newsup',
         BaseRegisterView.as_view(template_name='newsup.html'),
         name='newsup'),
    path('upgrade', UpgradeView.upgrade_me, name='upgrade'),
    path('<int:pk>/subscription_category', subscribe_category, name='subscribe_category'),
    path('<int:pk>/unsubscription_category', unsubscribe_category, name='unsubscribe_category'),
    path('categories', Categories.as_view()),
    path('subscription', Subscription.as_view()),
    path('categories/<int:pk>/news_in_category', PostsInCategoryList.as_view(), name='posts_in_category'),
    path('i18n/', include('django.conf.urls.i18n')),
]
