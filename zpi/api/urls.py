from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers

from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
]