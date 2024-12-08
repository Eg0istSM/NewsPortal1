"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news import views
#from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView


router = routers.DefaultRouter()
router.register(r'news', views.PostNewsViewest, basename='news')
router.register(r'article', views.PostArticleViewset, basename='article')


urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('post/', include('news.urls')),
   path('accounts/', include('allauth.urls')),
   path('sign/', include('sign.urls')),
   path('', include('protect.urls')),
   path('i18n/', include('django.conf.urls.i18n')),
   path('api/', include(router.urls)),
   path('api-auth/', include(arg='rest_framework.urls', namespace='rest_framework')),
   # path('swagger-ui/', TemplateView.as_view(
   #     template_name='swagger-ui.html',
   #     extra_context={'schema_url': 'openapi-schema'}
   # ), name='swagger-ui'),
]
