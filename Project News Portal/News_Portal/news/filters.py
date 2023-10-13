from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import *


# создаём фильтр
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author__user': ['exact'],
            'title': ['icontains'],
            # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
            'created_at': ['gt'],
            # количество товаров должно быть больше или равно тому, что указал пользователь
        }
        # labels = {
        #     'author__user': 'Автор',
        #     'title': 'Заголовок',
        #     'created_at': 'Дата создания(не позднее)',
        # }
