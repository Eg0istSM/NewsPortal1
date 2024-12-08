from .models import *
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Author
        fields = ['username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'text'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    time_post = serializers.DateTimeField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'text', 'time_post', 'rating', ]

