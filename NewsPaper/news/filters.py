import django_filters
from .models import Post, Author, Category
from django import forms


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    author = django_filters.ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), empty_label='Все авторы', label='Автор')
    date_after = django_filters.DateFilter(
        field_name='time_post', lookup_expr='gt', label='Дата после', widget=forms.DateInput(attrs={'type': 'date'}))
    category = django_filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all(), empty_label='Все категории', label='Категория')

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_after', 'category']

