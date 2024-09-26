from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-time_post'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time_post'
    template_name = 'flatpages/post_search.html'
    context_object_name = 'postsearch'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def det_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
