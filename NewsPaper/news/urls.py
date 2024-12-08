from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
from rest_framework import routers
from news import views


router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewset)
router.register(r'news', views.PostNewsViewest)
router.register(r'article', views.PostArticleViewset)
router.register(r'comment', views.CommentViewset)


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', PostsList.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('<int:pk>/like/', like, name='like'),
   path('<int:pk>/dislike/', dislike, name='dislike'),
   path('<int:pk>/comment/', PostComment.as_view(), name='post_comment'),
]
