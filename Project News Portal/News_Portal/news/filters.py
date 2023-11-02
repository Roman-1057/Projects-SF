import django_filters
from .models import *


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='Название', lookup_expr='icontains')
    author__user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Автор')
    created_at = django_filters.DateFilter(label='Дата создания(посты, после ГГГГ-ММ-ДД)', lookup_expr='gt')

    class Meta:
        model = Post
        fields = []

