from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, SearchPost, CreatePost


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view()),
   path('search', SearchPost.as_view(), name='search_post'),
   path('create_post', CreatePost.as_view(), name='create_post'),
   # path('', PostsList.post_sort, name='post_sort'),
   path('<int:pk>', PostDetail.as_view()),
   path('<int:pk>', PostDetail.post_detail, name='post_detail')
]
