import django_filters
from .models import Post, Author, Category
from django import forms
from django.utils.translation import gettext as _


# фильтр для страницы поиска постов
class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label=_('Название'))
    author = django_filters.ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), empty_label=_('Все авторы'), label=_('Автор'))
    date_after = django_filters.DateFilter(
        field_name='time_post', lookup_expr='gt', label=_('Дата после'), widget=forms.DateInput(attrs={'type': 'date'}))
    category = django_filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all(), empty_label=_('Все категории'), label=_('Категория'))

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_after', 'category']

