from django.urls import path
from .views import PostsList, PostDetail, PostCreate


urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', PostsList.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
]
