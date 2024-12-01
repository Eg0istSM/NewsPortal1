from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Post, Comment
from datetime import date


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get('author')
        today = date.today()
        post_limit = Post.objects.filter(author=author, time_post__date=today).count()
        if post_limit >= 3:
            raise ValidationError(_('Нельзя публиковать более трех постов в сутки!'))
        return cleaned_data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
