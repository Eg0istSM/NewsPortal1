from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            # 'author__name': ['icontains'],
            'time_post': ['gt'],
        }
