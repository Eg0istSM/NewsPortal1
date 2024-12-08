import pytz
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.response import Response

from .filters import PostFilter
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework import permissions
from .serializers import *
from .models import *


class PostsList(ListView):
    model = Post
    ordering = '-time_post'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def get_template_names(self):
        if self.request.path == '/post/search/':
            return 'flatpages/post_search.html'
        return 'flatpages/posts.html'

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META['HTTP_REFERER'])


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/post/articles/create/':
            post.post_type = 'AR'
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'
    permission_required = ('news.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_post_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_post')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = _('Вы успешно подписались на рассылку')
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})


def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like()
    post.save()
    return render(request, 'flatpages/post.html', {'post': post})


def dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.dislike()
    post.save()
    return render(request, 'flatpages/post.html', {'post': post})


class PostComment(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'flatpages/comment.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Post.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


# IsAdminUser - для админов ,IsAuthenticated - для авторизованных, AllowAny - открытый доступ.
class PostNewsViewest(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='NE')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user.author
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='AR')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

