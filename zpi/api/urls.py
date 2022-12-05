from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers

from .views import user_login, user_logout, change_password, get_applications, get_user_applications

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('get_applications/', get_applications, name="get_applications"),
    path('get_user_applications/', get_user_applications, name="get_user_applications"),
]
