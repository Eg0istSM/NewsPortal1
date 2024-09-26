from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch


urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
]
