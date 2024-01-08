from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from news import views

router = routers.DefaultRouter()
router.register(r'author', views.AuthorViewset)
router.register(r'post', views.PostViewest)
router.register(r'postcategory', views.PostCategoryViewest)
router.register(r'category', views.CategoryViewset)
router.register(r'comment', views.CommentViewest)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('articles_list/', views.ArticleListView.as_view(), name='article_list'),
    path('', include(router.urls)),
]
