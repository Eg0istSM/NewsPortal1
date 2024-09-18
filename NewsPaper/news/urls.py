from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail


urlpatterns = [
   path('', PostsList.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view()),
]
