from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, SearchPost, CreatePost, PostUpdate, PostDelete


urlpatterns = [
   path('', PostsList.as_view()),
   path('search', SearchPost.as_view(), name='search_post'),
   path('add', CreatePost.as_view(), name='create_post'),
   path('<int:pk>', PostDetail.as_view()),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>', PostDetail.post_detail, name='post_detail')
]
