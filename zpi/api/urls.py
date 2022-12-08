from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers

from .views import user_login, user_logout, change_password, ShortApplicationListView, \
    ApplicationListView, ApplicationView, DepartmentListView, ApplicationPropertyListView, UserApplicationCreateView, UserApplicationsListListView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change_password/', change_password, name='change_password'),

    path('get_applications/', ShortApplicationListView.as_view(), name="get_applications"),
    path('get_departments/', DepartmentListView.as_view(), name="get_departments"),

    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('application/<int:id>/', ApplicationView.as_view(), name='application'),
    path('application/<int:id>/properties/', ApplicationPropertyListView.as_view(), name='application-properties'),

    path('user/application/<int:id>/', UserApplicationCreateView.as_view(), name='user-application'),
    path('user_applications/', UserApplicationsListListView.as_view(), name="user_applications"),

]
