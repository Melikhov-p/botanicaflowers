"""
URL configuration for botanicaflowers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from chats.views import ChatView, MessageView
from client.views import ClientView, login
from goods.views import ProductView, LikeView, CategoryView, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/login/', login, name='login'),
    path('', index),
]

router = routers.DefaultRouter()
router.register(r'api/clients', ClientView, 'clients')
router.register(r'api/category', CategoryView, 'category')
router.register(r'api/products', ProductView, 'products')
router.register(r'api/likes', LikeView, 'likes')
router.register(r'api/chats', ChatView, basename='chats')
router.register(r'api/messages', MessageView, basename='messages')

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
