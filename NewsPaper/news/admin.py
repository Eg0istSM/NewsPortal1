from django.contrib import admin
from .models import Category, Post


# удобный вывод в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'time_post')  # генерация списка всех имен полей(можно просто имена полей)
    list_filter = ('category', 'author', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'author__user__username')  # поиск по названию и автору


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
