from django_filters import FilterSet
from .models import *


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author__user': ['exact'],
            'title': ['icontains'],
            'created_at': ['gt'],
        }

