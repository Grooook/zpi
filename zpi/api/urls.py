from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers

from .views import LoginView, get_applications, get_user_applications

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('get_applications/', get_applications, name="get_applications"),
    path('get_user_applications/', get_user_applications, name="get_user_applications"),
]